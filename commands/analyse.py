# analyse.py
import requests
import pandas as pd
from datetime import datetime, timedelta

def analyse(symbol, days):
    """
    Analyse the price of a cryptocurrency over a specified period.
    
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT').
        days (int): The number of days to look back for analysis.
    """
    # Convert the days into milliseconds for the Binance API
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval=1d&startTime={start_time}&endTime={end_time}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if not data:
            print(f"No data available for {symbol.upper()} for the last {days} days.")
            return

        # Extract relevant data (timestamp, open, high, low, close prices)
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
            'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Convert price columns to float
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)

        # Calculate statistics
        start_price = df['close'].iloc[0]
        end_price = df['close'].iloc[-1]
        percentage_change = ((end_price - start_price) / start_price) * 100
        highest_price = df['high'].max()
        lowest_price = df['low'].min()

        # Convert timestamps to readable dates
        start_date = datetime.fromtimestamp(start_time / 1000).strftime('%Y-%m-%d')
        end_date = datetime.fromtimestamp(end_time / 1000).strftime('%Y-%m-%d')

        # Define colors
        BOLD = '\033[1m'
        RESET = '\033[0m'
        GREEN = '\033[1;92m'
        RED = '\033[1;91m'

        # Determine color based on percentage change
        color = GREEN if percentage_change > 0 else RED

        # Print introduction with dates and symbol
        print(f"\nAnalyzing {symbol.upper()} from {start_date} to {end_date}:")

        # Display statistics
        print(f"{BOLD}Evolution: {RESET}{color}{percentage_change:.2f}%{RESET}")
        print(f"{BOLD}Highest Price:{RESET} {highest_price:.2f}")
        print(f"{BOLD}Lowest Price:{RESET} {lowest_price:.2f}")
        print(f"{BOLD}Start Price:{RESET} {start_price:.2f}")
        print(f"{BOLD}End Price:{RESET} {end_price:.2f}")
        print("")

    except Exception as e:
        print(f"An error occurred: {e}")
