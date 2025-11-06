# src/basic_bot.py
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)

class BasicBot:
    """
    Minimal REST client for Binance USDT-M Futures Testnet.
    Uses HMAC SHA256 signing for private endpoints (orders).
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, base_url: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        # testnet base URL for USDT-M futures
        self.base_url = base_url or (
            "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        )
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })
        logger.debug(f"BasicBot initialized with base_url={self.base_url}")

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _signed_request(self, method: str, path: str, params: dict):
        """
        Signed request (for endpoints requiring user signature).
        Logs request/response.
        """
        params = params or {}
        params['timestamp'] = self._get_timestamp()
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        params['signature'] = signature

        url = self.base_url.rstrip('/') + path
        logger.info(f"REQUEST -> {method} {url} | params: {params}")
        try:
            if method.upper() == "POST":
                resp = self.session.post(url, data=params, timeout=10)
            elif method.upper() == "DELETE":
                resp = self.session.delete(url, params=params, timeout=10)
            else:
                resp = self.session.get(url, params=params, timeout=10)
            logger.info(f"RESPONSE <- {resp.status_code} {resp.text}")
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            logger.exception("HTTP error on signed request")
            raise

    def _public_request(self, path: str, params: dict = None):
        url = self.base_url.rstrip('/') + path
        logger.info(f"PUBREQ -> GET {url} | params: {params}")
        try:
            resp = self.session.get(url, params=params, timeout=10)
            logger.info(f"PUBRESP <- {resp.status_code} {resp.text}")
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            logger.exception("HTTP error on public request")
            raise

    # Core: place order
    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float = None, price: float = None,
                    timeInForce: str = "GTC", stopPrice: float = None, reduceOnly: bool = False):
        """
        Places an order on futures.
        - symbol: e.g., "BTCUSDT"
        - side: BUY or SELL
        - order_type: MARKET, LIMIT, STOP, TAKE_PROFIT, etc.
        - quantity: required for MARKET/LIMIT/STOP
        - price: required for LIMIT/STOP/TAKE_PROFIT
        - stopPrice: used for STOP/TAKE_PROFIT
        """
        path = "/fapi/v1/order"
        side = side.upper()
        order_type = order_type.upper()

        params = {
            "symbol": symbol.upper(),
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        # Include price for LIMIT, STOP (Stop-Limit), and TAKE_PROFIT
        if order_type in ["LIMIT", "STOP", "TAKE_PROFIT"]:
            if price is None:
                raise ValueError(f"{order_type} orders require price")
            params.update({"price": price, "timeInForce": timeInForce})

        # Include stopPrice for STOP and TAKE_PROFIT types
        if stopPrice is not None:
            params["stopPrice"] = stopPrice

        # remove None values
        params = {k: v for k, v in params.items() if v is not None}

        # convert all floats to strings (Binance requires strings for numbers)
        for k, v in list(params.items()):
            if isinstance(v, float):
                params[k] = format(v, 'f')

        logger.debug(f"Placing order with params: {params}")
        res = self._signed_request("POST", path, params)
        return res

    def ping(self):
        return self._public_request("/fapi/v1/ping")

    def get_server_time(self):
        return self._public_request("/fapi/v1/time")
