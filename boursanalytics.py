#!/usr/bin/env python3

import os
import readline
import shlex

from commands.getprice import get_price
from commands.analyse import analyse

def show_banner():
    """Displays the ASCII art and information."""
    BLUE = '\033[94m'
    RESET = '\033[0m'

    banner = BLUE + """
 ____                          _                _       _   _          
| __ )  ___  _   _ _ __ ___   / \\   _ __   __ _| |_   _| |_(_) ___ ___ 
|  _ \\ / _ \\| | | | '__/ __| / _ \\ | '_ \\ / _ | | | | | __| |/ __/ __|
| |_) | (_) | |_| | |  \\__ \\/ ___ \\| | | | (_| | | |_| | |_| | (__\\__ \\
|____/ \\___/ \\__,_|_|  |___/_/   \\_\\_| |_|\\__,_|_|\\__, |\\__|_|\\___|___/
                                                  |___/                
    """ + RESET

    info_text = """
    Welcome to BoursAnalytics!
    This program helps you track stock prices.
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
                    get_price(stock_symbol)  # Appel de la fonction avec le symbole de la crypto-monnaie
                else:
                    print("Usage: getprice <stock_symbol>")
            elif command == "help":
                show_banner()  # Re-display the banner as help message
            
            elif command == "analyse":
                if len(args) > 1:
                    # Extraction des options -s et -t
                    symbol = None
                    time_period = 30  # Valeur par défaut, par exemple 30 jours

                    for arg in args[1:]:
                        if arg.startswith('-s'):
                            symbol = arg[2:].upper()  # Extraire le symbole après -s
                        elif arg.startswith('-t'):
                            try:
                                time_period = int(arg[2:])  # Extraire le nombre de jours après -t
                            except ValueError:
                                print("Invalid time period. Please enter a number.")
                                continue
                    
                    if symbol:
                        analyse(symbol, time_period)
                    else:
                        print("Usage: analyse -s[symbol] -t[time in days]")
                else:
                    print("Usage: analyse -s[symbol] -t[time in days]")
                    
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
