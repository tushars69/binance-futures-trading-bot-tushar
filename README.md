# 🌐 Simplified Binance Futures Testnet Trading Bot

### 🚀 Overview
This is a **lightweight, modular CLI-based trading bot** built in **Python** that connects to the **Binance USDT-M Futures Testnet** via REST API.  
It supports placing **MARKET**, **LIMIT**, and **STOP-LIMIT** orders using HMAC-SHA256 authentication.

Developed as part of the **Junior Python Developer – Crypto Trading Bot** internship assignment.

---

## 🧩 Features
✅ Place **Market Orders**  
✅ Place **Limit Orders**  
✅ Place **Stop-Limit Orders (Advanced)**  
✅ Supports **Buy/Sell** sides  
✅ Secure **API key handling via `.env`**  
✅ Detailed **logging (`bot.log`)** of requests/responses  
✅ Modular, reusable **code structure**  
✅ CLI interface for quick testing  

---

## 🗂️ Project Structure

project_root/
├── src/
│ ├── init.py
│ ├── basic_bot.py # Core Binance REST client
│ ├── market_orders.py # Handles market orders
│ ├── limit_orders.py # Handles limit orders
│ ├── cli.py # CLI entry point
│ └── advanced/
│ ├── init.py
│ └── stop_limit.py # Stop-Limit (advanced order)
├── bot.log # Auto-created log file
├── .env # API credentials (excluded from version control)
└── README.md


---

## ⚙️ Requirements
- Python **3.8+**
- Install dependencies:
  ```bash
  pip install requests python-dotenv

