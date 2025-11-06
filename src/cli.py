# src/cli.py
import argparse
import os
import logging
from market_orders import place_market
from limit_orders import place_limit
from advanced.stop_limit import place_stop_limit
from dotenv import load_dotenv
load_dotenv()

# Configure root logger to write to bot.log
LOGFILE = os.path.join(os.path.dirname(__file__), "..", "bot.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOGFILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("trading_bot_cli")

def parse_args():
    p = argparse.ArgumentParser(description="Simple Binance Futures Testnet Trading CLI")
    p.add_argument("order_type", choices=["MARKET","LIMIT","STOP_LIMIT"], help="Order type")
    p.add_argument("symbol", help="Symbol, e.g., BTCUSDT")
    p.add_argument("side", choices=["BUY","SELL"], help="BUY or SELL")
    p.add_argument("quantity", type=float, help="Quantity (in contract size)")
    p.add_argument("--price", type=float, default=None, help="Price for LIMIT or STOP_LIMIT")
    p.add_argument("--stop", type=float, default=None, help="Stop price for STOP_LIMIT")
    p.add_argument("--api_key", default=os.getenv("BINANCE_API_KEY"), help="Binance API Key (or env BINANCE_API_KEY)")
    p.add_argument("--api_secret", default=os.getenv("BINANCE_API_SECRET"), help="Binance API Secret (or env BINANCE_API_SECRET)")
    p.add_argument("--testnet", action="store_true", default=True, help="Use testnet (default True)")
    return p.parse_args()

def validate_args(args):
    if not args.api_key or not args.api_secret:
        raise ValueError("API key/secret required. Set BINANCE_API_KEY and BINANCE_API_SECRET env vars or pass --api_key/--api_secret.")
    if args.order_type == "LIMIT" and args.price is None:
        raise ValueError("LIMIT orders require --price")
    if args.order_type == "STOP_LIMIT" and (args.price is None or args.stop is None):
        raise ValueError("STOP_LIMIT requires --price and --stop")
    if args.quantity <= 0:
        raise ValueError("Quantity must be > 0")

def main():
    args = parse_args()
    try:
        validate_args(args)
    except Exception as e:
        logger.error("Validation error: %s", e)
        return

    logger.info("Placing %s order for %s %s qty=%s price=%s stop=%s", args.order_type, args.side, args.symbol, args.quantity, args.price, args.stop)

    try:
        if args.order_type == "MARKET":
            res = place_market(args.api_key, args.api_secret, args.symbol, args.side, args.quantity, testnet=args.testnet)
        elif args.order_type == "LIMIT":
            res = place_limit(args.api_key, args.api_secret, args.symbol, args.side, args.quantity, args.price, testnet=args.testnet)
        elif args.order_type == "STOP_LIMIT":
            res = place_stop_limit(args.api_key, args.api_secret, args.symbol, args.side, args.quantity, args.stop, args.price, testnet=args.testnet)
        else:
            raise ValueError("Unsupported order type")

        logger.info("ORDER RESULT: %s", res)
        print("Order placed. Exchange response:")
        print(res)
    except Exception as e:
        logger.exception("Failed to place order: %s", e)
        print(f"Error placing order: {e}")

if __name__ == "__main__":
    main()
