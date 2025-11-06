# src/limit_orders.py
import logging
from basic_bot import BasicBot

logger = logging.getLogger(__name__)

def place_limit(api_key, api_secret, symbol, side, quantity, price, timeInForce="GTC", testnet=True):
    bot = BasicBot(api_key, api_secret, testnet=testnet)
    try:
        res = bot.place_order(symbol=symbol, side=side, order_type="LIMIT", quantity=quantity, price=price, timeInForce=timeInForce)
        logger.info("Limit order placed: %s", res)
        return res
    except Exception as e:
        logger.exception("Failed to place limit order")
        raise
