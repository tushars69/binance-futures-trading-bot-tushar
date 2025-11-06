# data/collect_candles.py
import os, time, requests, pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
OUT = "data/candles_BTCUSDT.csv"

def fetch_klines(symbol=SYMBOL, interval=INTERVAL, limit=1000):
    url = f"{BASE}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def save_to_csv(rows):
    df = pd.DataFrame(rows, columns=["open_time","open","high","low","close","volume",
                                     "close_time","q","n","taker_base","taker_quote","ignore"])
    df["close"] = df["close"].astype(float)
    df.to_csv(OUT, index=False)

if __name__ == "__main__":
    rows = fetch_klines()
    save_to_csv(rows)
    print("Saved", OUT)
