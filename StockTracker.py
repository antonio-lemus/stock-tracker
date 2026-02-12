import yfinance as yf
import requests
import os
import sys
import time
import random

# --- CONFIGURATION ---
# We get these from GitHub "Secrets" (Environment Variables)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Error: Secrets not found. Make sure you added them in GitHub Settings.")
    sys.exit(1)

# Dynamic Targets (Percent of 5-Day Average)
WATCHLIST = {
    "QQQM":  {"buy_pct": 1.01, "sell_pct": 1.01},
    "VOO":   {"buy_pct": 0.99, "sell_pct": 1.01},
    "LMT":   {"buy_pct": 0.96, "sell_pct": 1.03},
    "CRWD":  {"buy_pct": 0.95, "sell_pct": 1.04},
    "CVX":   {"buy_pct": 0.96, "sell_pct": 1.03},
    "LLY":   {"buy_pct": 0.96, "sell_pct": 1.03},
    "UBER":  {"buy_pct": 0.95, "sell_pct": 1.04},
    "TSLA":  {"buy_pct": 0.95, "sell_pct": 1.4},
    "NVDA":  {"buy_pct": 0.95, "sell_pct": 1.03},
    "AMZN":  {"buy_pct": 0.98, "sell_pct": 1.03},
    "GOOGL": {"buy_pct": 0.98, "sell_pct": 1.03}
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def get_data(ticker):
    try:
        # Get 5 days of history to calculate average
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        
        if hist.empty:
            return None, None
            
        avg_price = hist['Close'].mean()
        # Get the very latest price (regularMarketPrice is safer for scripts)
        current_price = stock.fast_info['last_price']
        
        return current_price, avg_price
    except Exception as e:
        print(f"⚠️ Could not fetch data for {ticker}: {e}")
        return None, None

def main():
    print("🚀 Running One-Time Check...")
    
    # 1. Random delay (1-15s) to avoid "bot" detection blocks
    time.sleep(random.randint(1, 15))

    alerts_sent = 0
    
    for ticker, settings in WATCHLIST.items():
        price, avg_price = get_data(ticker)
        
        if not price or not avg_price:
            continue

        buy_target = avg_price * settings["buy_pct"] if settings["buy_pct"] else 0
        sell_target = avg_price * settings["sell_pct"] if settings["sell_pct"] else 999999

        print(f"{ticker}: ${price:.2f} (Avg: ${avg_price:.2f})")

        # --- LOGIC ---
        if price <= buy_target:
            pct_drop = ((avg_price - price) / avg_price) * 100
            msg = (f"📉 **BUY ALERT: {ticker}**\n"
                   f"Price: ${price:.2f}\n"
                   f"Avg: ${avg_price:.2f}\n"
                   f"Discount: -{pct_drop:.1f}%")
            send_telegram_message(msg)
            alerts_sent += 1
            
        elif price >= sell_target:
            pct_gain = ((price - avg_price) / avg_price) * 100
            msg = (f"📈 **SELL ALERT: {ticker}**\n"
                   f"Price: ${price:.2f}\n"
                   f"Avg: ${avg_price:.2f}\n"
                   f"Gain: +{pct_gain:.1f}%")
            send_telegram_message(msg)
            alerts_sent += 1

    if alerts_sent > 0:
        print(f"✅ Sent {alerts_sent} alerts.")
    else:
        print("✅ No alerts triggered this run.")

if __name__ == "__main__":
    main()