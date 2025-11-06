# src/mcp_server.py
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os, requests, json
from basic_bot import BasicBot
from market_orders import place_market_order   # ensure this function exists and is importable

load_dotenv()

app = FastAPI(title="Binance MCP Server", version="1.0")
mcp = FastMCP(app)

PREDICT_URL = os.getenv("PREDICT_URL", "http://127.0.0.1:8501/predict")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

@mcp.tool()
def get_bot_status():
    """Return last 5 lines of bot.log"""
    try:
        if not os.path.exists("bot.log"):
            return {"status": "error", "message": "No bot.log file found."}
        with open("bot.log", "r") as f:
            logs = f.readlines()[-5:]
        return {"status": "running", "recent_logs": logs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def model_signal(symbol: str):
    """Call local model service to get a signal"""
    # For a real system you'd compute features from latest candles before calling
    sample_payload = {"close": 1.0, "ma3": 1.0, "ma8": 1.0, "ret": 0.0}
    r = requests.post(PREDICT_URL, json=sample_payload, timeout=5)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def ai_decide_and_trade(symbol: str, qty: float = 0.001):
    """Ask LLM to decide and optionally place a trade if confidence high."""
    import openai
    openai.api_key = OPENAI_KEY
    # fetch a model signal first
    sig = model_signal(symbol)
    prompt = f"Signal: {sig}. Given this, advise BUY/SELL/HOLD in single word and why (short)."
    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=150)
    text = resp["choices"][0]["message"]["content"].strip()
    decision = "HOLD"
    if "BUY" in text.upper():
        decision = "BUY"
    elif "SELL" in text.upper():
        decision = "SELL"

    result = {"ai_text": text, "decision": decision}
    # safety check
    if decision in ["BUY","SELL"] and sig.get("confidence", 0) > 0.6:
        try:
            place_res = place_market_order(symbol, decision, qty)
            result["trade"] = place_res
        except Exception as e:
            result["trade_error"] = str(e)
    else:
        result["trade"] = "no_trade_due_to_confidence_or_hold"
    return result

if __name__ == "__main__":
    import uvicorn
    print("MCP Server running at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
