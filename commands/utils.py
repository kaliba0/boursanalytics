# utils.py
import json

def load_portfolio(file_path):
    """
    Loads the portfolio data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        dict: The portfolio data.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return None

def save_portfolio(file_path, data):
    """
    Saves the portfolio data to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
        data (dict): The portfolio data to save.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving portfolio: {e}")
