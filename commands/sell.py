# sell.py
import requests
from datetime import datetime
from .utils import load_portfolio, save_portfolio

PORTFOLIO_FILE = 'portfolio.json'

def sell(symbol, amount):
    """
    Sells a specified amount of a cryptocurrency from the portfolio.
    
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT').
        amount (float or str): The amount of the cryptocurrency units to sell, or '*' to sell all units.
    """
    portfolio = load_portfolio(PORTFOLIO_FILE)

    if not portfolio:
        print("Portfolio not found. Please initialize it first.")
        return

    if symbol not in portfolio['investments']:
        print(f"No investments found for {symbol}.")
        return

    # If amount is '*', sell all units of the specified symbol
    if amount == "*":
        amount = portfolio['investments'][symbol]['units']
    
    # Check if the amount to sell is available
    if portfolio['investments'][symbol]['units'] < amount:
        print(f"Insufficient units to sell. You have {portfolio['investments'][symbol]['units']} units of {symbol}.")
        return

    # Fetch the current price of the cryptocurrency
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        data = response.json()
        current_price = float(data['price'])

        # Calculate the total value of the sale
        total_value = amount * current_price

        # Update the portfolio
        portfolio['investments'][symbol]['units'] -= amount
        if portfolio['investments'][symbol]['units'] <= 0:
            del portfolio['investments'][symbol]  # Remove the investment if no units are left
        portfolio['balance'] += total_value

        # Log the transaction
        transaction = {
            "type": "sell",
            "symbol": symbol,
            "units_sold": amount,
            "price_per_unit": current_price,
            "total_received": total_value,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        portfolio['transactions'].append(transaction)

        # Save updated portfolio
        save_portfolio(PORTFOLIO_FILE, portfolio)
        print(f"Successfully sold {amount} units of {symbol}. Total received: {total_value:.2f} euros.")

    except Exception as e:
        print(f"Error fetching price or processing sale: {e}")
