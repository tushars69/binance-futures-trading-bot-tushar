# src/advanced/stop_limit.py
import logging
from basic_bot import BasicBot

logger = logging.getLogger(__name__)

def place_stop_limit(api_key, api_secret, symbol, side, quantity, stopPrice, price, testnet=True):
    """
    Places a Stop-Limit order on Binance Futures.
    Requires: stopPrice + price + timeInForce
    """
    bot = BasicBot(api_key, api_secret, testnet=testnet)
    try:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "order_type": "STOP",          # Correct type for Futures Stop-Limit
            "quantity": quantity,
            "price": price,
            "stopPrice": stopPrice,
            "timeInForce": "GTC",          # must be added for stop-limit
        }

        # Use BasicBot directly for REST POST
        res = bot.place_order(
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
            stopPrice=params["stopPrice"],
            timeInForce=params["timeInForce"],
        )

        logger.info("✅ Stop-Limit order placed: %s", res)
        return res

    except Exception as e:
        logger.exception("❌ Failed to place stop-limit order")
        raise
