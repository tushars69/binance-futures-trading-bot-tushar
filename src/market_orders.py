# src/market_orders.py
import logging
from basic_bot import BasicBot

logger = logging.getLogger(__name__)

def place_market(api_key, api_secret, symbol, side, quantity, testnet=True):
    """
    Places a MARKET order using the BasicBot class.
    """
    bot = BasicBot(api_key, api_secret, testnet=testnet)
    try:
        res = bot.place_order(
            symbol=symbol,
            side=side,
            order_type="MARKET",
            quantity=quantity
        )
        logger.info("Market order placed: %s", res)
        return res
    except Exception as e:
        logger.exception("Failed to place market order")
        raise
