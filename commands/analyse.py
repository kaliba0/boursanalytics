# analyse.py
import requests
from datetime import datetime, timedelta

def analyse(symbol, days):
    """
    Analyze the cryptocurrency data over the given number of days.

    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT' for Bitcoin).
        days (int): The number of days for the analysis.
    """
    # Calculer la date de début pour récupérer les données historiques
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Convertir les dates en millisecondes pour l'API de Binance
    end_time_ms = int(end_time.timestamp() * 1000)
    start_time_ms = int(start_time.timestamp() * 1000)

    # URL pour récupérer les données de klines (historique des prix) sur la période donnée
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval=1d&startTime={start_time_ms}&endTime={end_time_ms}"

    try:
        response = requests.get(url)
        data = response.json()

        if not data:
            print(f"No data available for {symbol.upper()} in the past {days} days.")
            return

        # Extraction des prix pour les calculs
        open_prices = [float(item[1]) for item in data]  # Prix d'ouverture
        close_prices = [float(item[4]) for item in data]  # Prix de fermeture
        high_prices = [float(item[2]) for item in data]  # Prix le plus haut
        low_prices = [float(item[3]) for item in data]  # Prix le plus bas

        # Calculs des statistiques
        percentage_change = ((close_prices[-1] - open_prices[0]) / open_prices[0]) * 100
        highest_price = max(high_prices)
        lowest_price = min(low_prices)
        average_price = sum(close_prices) / len(close_prices)

        # Affichage des résultats
        print(f"Analysis of {symbol.upper()} over the last {days} days:")
        print(f"Percentage change: {percentage_change:.2f}%")
        print(f"Highest price: {highest_price:.2f} USD")
        print(f"Lowest price: {lowest_price:.2f} USD")
        print(f"Average closing price: {average_price:.2f} USD")

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
