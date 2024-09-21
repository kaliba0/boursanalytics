# getprice.py
import requests
import time
import sys

def get_price(symbol):

    """
    Fetches and displays the current price of a cryptocurrency in real-time.
    
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT' for Bitcoin in USD).
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    
    try:
        while True:
            response = requests.get(url)
            data = response.json()
            
            if 'price' in data:
                price = float(data['price'])
                sys.stdout.write(f"\rCurrent price of {symbol.upper()}: {price:.2f} EUR")
                sys.stdout.flush()
                time.sleep(0.1)  # Sleep for 100 milliseconds
            else:
                print(f"Error fetching data: {data}")
                break
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
