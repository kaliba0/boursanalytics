# addmoney.py
import json
from datetime import datetime
from .utils import load_portfolio, save_portfolio

PORTFOLIO_FILE = 'portfolio.json'

def add_money(amount):
    """
    Adds a specified amount of money to the portfolio and logs the transaction.
    
    Args:
        amount (float): The amount of money to add.
    """
    try:
        # Charge les données du portefeuille depuis le fichier JSON
        portfolio = load_portfolio(PORTFOLIO_FILE)

        if not portfolio:
            print("Portfolio not found. Please initialize it first.")
            return

        # Ajoute le montant au solde actuel
        portfolio['balance'] += amount

        # Enregistre la transaction avec la date et l'heure
        transaction = {
            "type": "add_money",
            "amount": amount,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "new_balance": portfolio['balance']
        }
        portfolio['transactions'].append(transaction)

        # Sauvegarde les données mises à jour dans le fichier JSON
        save_portfolio(PORTFOLIO_FILE, portfolio)

        print(f"Added {amount} euros to the portfolio. New balance: {portfolio['balance']} euros.")
    except Exception as e:
        print(f"Error adding money to portfolio: {e}")
