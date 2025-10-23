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
│   ├── basic_bot.py
│   ├── cli.py
│   ├── market_orders.py
│   ├── limit_orders.py
│   └── advanced/
│       └── stop_limit.py
├── bot.log
├── .env
└── README.md

---

## ⚙️ Requirements
- Python **3.8+**
- Install dependencies:
  ```bash
  pip install requests python-dotenv

