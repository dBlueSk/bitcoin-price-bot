from dotenv import load_dotenv
import os
import requests
import time
from datetime import datetime

# Load environment variables from .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
COINGECKO_API = os.getenv("COINGECKO_API")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def get_bitcoin_price():
    """Fetch Bitcoin price from CoinGecko API"""
    try:
        response = requests.get(COINGECKO_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['usd']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response: {e}")
        return None

def send_telegram_message(message):
    """Send message to Telegram channel"""
    try:
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return False

def main():
    """Main loop to fetch and send Bitcoin price every minute"""
    print("Bitcoin Price Monitor Started")
    print(f"Fetching from: {COINGECKO_API}")
    print(f"Sending to: {TELEGRAM_CHAT_ID}")
    print("-" * 50)
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            btc_price = get_bitcoin_price()
            
            if btc_price:
                message = f"💰 <b>Bitcoin Price Update</b>\n\n${btc_price:,.2f}"
                
                if send_telegram_message(message):
                    print(f"[{current_time}] ✓ Sent: ${btc_price:,.2f}")
                else:
                    print(f"[{current_time}] ✗ Failed to send message")
            else:
                print(f"[{current_time}] ✗ Failed to fetch price")
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n\nBot stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
