# portfolio.py
import json
from .utils import load_portfolio, save_portfolio

PORTFOLIO_FILE = 'portfolio.json'

def initialize_portfolio():
    """
    Initializes the portfolio with a base amount of 10,000 euros if it does not already exist.
    """
    portfolio = load_portfolio(PORTFOLIO_FILE)

    if not portfolio:
        # Initialize with 10,000 euros and empty investments
        portfolio = {
            "balance": 10000.0,
            "investments": {},  # Ajout de la clé 'investments' pour éviter les KeyError
            "transactions": []
        }
        save_portfolio(PORTFOLIO_FILE, portfolio)
        print("Portfolio initialized with 10,000 euros.")
    else:
        # Mise à jour du portefeuille existant s'il manque des clés
        if 'investments' not in portfolio:
            portfolio['investments'] = {}
        if 'transactions' not in portfolio:
            portfolio['transactions'] = []

        save_portfolio(PORTFOLIO_FILE, portfolio)
        print("Portfolio already initialized.")

def show_portfolio():
    """
    Displays the current balance and investments in the portfolio.
    """
    portfolio = load_portfolio(PORTFOLIO_FILE)

    if portfolio:
        print(f"Current Balance: {portfolio['balance']:.2f} euros")
        print("Investments:")
        if portfolio['investments']:
            for symbol, investment in portfolio['investments'].items():
                print(f"  {symbol}: {investment['units']} units, Total Invested: {investment['total_invested']} euros")
        else:
            print("  No investments yet.")
        print("Recent Transactions:")
        for transaction in portfolio['transactions']:
            print(transaction)
    else:
        print("Portfolio not found. Please initialize it first.")
