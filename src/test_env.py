from dotenv import load_dotenv
import os

# Load variables from .env automatically
load_dotenv()

print("API Key:", os.getenv("BINANCE_API_KEY"))
print("Secret Key:", os.getenv("BINANCE_API_SECRET"))
