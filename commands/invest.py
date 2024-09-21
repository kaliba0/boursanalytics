# invest.py
import requests
from datetime import datetime
from .utils import load_portfolio, save_portfolio

PORTFOLIO_FILE = 'portfolio.json'

def invest(symbol, amount):
    """
    Invests a specified amount in a cryptocurrency.
    
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT').
        amount (float): The amount to invest in euros.
    """
    portfolio = load_portfolio(PORTFOLIO_FILE)

    if not portfolio:
        print("Portfolio not found. Please initialize it first.")
        return

    if amount > portfolio['balance']:
        print("Insufficient funds to invest.")
        return

    # Fetch the current price of the cryptocurrency
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        data = response.json()
        price = float(data['price'])

        # Calculate units bought
        units_bought = amount / price

        # Update portfolio
        if symbol in portfolio['investments']:
            portfolio['investments'][symbol]['units'] += units_bought
            portfolio['investments'][symbol]['total_invested'] += amount
        else:
            portfolio['investments'][symbol] = {
                'units': units_bought,
                'total_invested': amount
            }

        portfolio['balance'] -= amount

        # Log the transaction
        transaction = {
            "type": "buy",
            "symbol": symbol,
            "amount": amount,
            "units": units_bought,
            "price_per_unit": price,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        portfolio['transactions'].append(transaction)

        # Save updated portfolio
        save_portfolio(PORTFOLIO_FILE, portfolio)
        print(f"Successfully invested {amount} euros in {symbol}. Units bought: {units_bought:.6f}")

    except Exception as e:
        print(f"Error fetching price or processing investment: {e}")
