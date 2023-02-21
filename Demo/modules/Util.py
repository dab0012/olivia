# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

from colorama import Style, Fore

RED = Fore.RED
GREEN = Fore.GREEN

# Function to print colored text
def print_colored(text, color ):
    print(color, end="")
    print(text, end="")
    print(Style.RESET_ALL)