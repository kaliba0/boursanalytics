#!/usr/bin/env python3

import os
import readline
import shlex

from commands.getprice import get_price
from commands.analyse import analyse
from commands.portfolio import initialize_portfolio, show_portfolio
from commands.addmoney import add_money
from commands.invest import invest
from commands.sell import sell

def show_banner():
    """Displays the ASCII art and information."""
    BLUE = '\033[94m'
    RESET = '\033[0m'

    banner = BLUE + r"""
██████╗  ██████╗ ██╗   ██╗██████╗ ███████╗ █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗████████╗██╗ ██████╗███████╗
██╔══██╗██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══██╔══╝██║██╔════╝██╔════╝
██████╔╝██║   ██║██║   ██║██████╔╝███████╗███████║██╔██╗ ██║███████║██║   ╚████╔╝    ██║   ██║██║     ███████╗
██╔══██╗██║   ██║██║   ██║██╔══██╗╚════██║██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝     ██║   ██║██║     ╚════██║
██████╔╝╚██████╔╝╚██████╔╝██║  ██║███████║██║  ██║██║ ╚████║██║  ██║███████╗██║      ██║   ██║╚██████╗███████║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═╝   ╚═╝ ╚═════╝╚══════╝

    """ + RESET

    info_text = """
    Welcome to BoursAnalytics!
    This program helps you track stock prices, analyze trends, and manage a virtual portfolio.
    Type 'getprice' followed by the stock symbol to get started.
    Example: getprice AAPL
    """

    print(banner)
    print(info_text)

def update_prompt():
    """Returns the appropriate prompt."""
    BLUE_BOLD = '\033[1;94m'
    RESET = '\033[0m'
    return f"{BLUE_BOLD}boursanalytics>{RESET} "

def main():
    os.system('clear')  # Clear screen when starting the application
    show_banner()
    initialize_portfolio()

    # Enable command history and configure readline
    readline.set_auto_history(True)  # Automatically adds commands to history

    # Initialize prompt
    prompt = update_prompt()  # Set initial prompt

    # Main application loop
    while True:
        try:
            # Read user input
            user_input = input(prompt).strip()
            
            # Parse the command using shlex to handle quoted strings properly
            args = shlex.split(user_input)
            
            if not args:
                continue

            command = args[0].lower()  # Get the command (first word)
            
            if command == "getprice":
                if len(args) > 1:
                    stock_symbol = args[1]
                    get_price(stock_symbol)  # Call get_price function with the stock symbol
                else:
                    print("Usage: getprice <stock_symbol>")
            elif command == "help":
                show_banner()  # Re-display the banner as help message
            
            elif command == "analyse":
                if len(args) > 4 and args[1] == "-s" and args[3] == "-t":
                    symbol = args[2]
                    try:
                        days = int(args[4])
                        analyse(symbol, days)  # Call analyse function with the parameters
                    except ValueError:
                        print("Invalid time period. Please enter a number.")
                else:
                    print("Usage: analyse -s <symbol> -t <time_in_days>")
            elif command == "addmoney":
                if len(args) > 1:
                    try:
                        amount = float(args[1])
                        add_money(amount)  # Add money to the portfolio
                    except ValueError:
                        print("Invalid amount. Please enter a number.")
                else:
                    print("Usage: addmoney <amount>")
            elif command == "portfolio":
                show_portfolio()  # Show current portfolio
            elif command == "sell":
                if len(args) > 4 and args[1] == "-s" and args[3] == "-a":
                    symbol = args[2]
                    amount = args[4]
                    if amount == "*":
                        sell(symbol, "*")  # Sell all units of the specified cryptocurrency
                    else:
                        try:
                            amount = float(amount)
                            sell(symbol, amount)  # Sell the specified amount of the cryptocurrency
                        except ValueError:
                            print("Invalid amount. Please enter a number or '*' to sell all.")
                else:
                    print("Usage: sell -s <symbol> -a <amount>")
            elif command == "invest":
                if len(args) > 4 and args[1] == "-s" and args[3] == "-a":
                    symbol = args[2]
                    try:
                        amount = float(args[4])
                        invest(symbol, amount)  # Invest in a cryptocurrency
                    except ValueError:
                        print("Invalid amount. Please enter a number.")
                else:
                    print("Usage: invest -s <symbol> -a <amount>")
            elif command == "exit":
                print("Goodbye!")
                break
            else:
                print("Unknown command. Type 'help' to see available commands.")

        except KeyboardInterrupt:
            # Handle Ctrl+C interruption
            print("\nInterrupt: use the 'exit' command to quit.")
        except EOFError:
            # Handle Ctrl+D or other EOF errors
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
