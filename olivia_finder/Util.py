# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

from colorama import Style, Fore

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE

# Function to print colored text
def print_colored(text, color):
    print(color, end="")
    print(text, end="")
    print(Style.RESET_ALL)

def clean_string(s: str):
    '''
    Clean a string from whitespaces and newlines

    Parameters
    ----------
    string : str
        String to be cleaned

    Returns
    -------
    str
        Cleaned string
    '''
    s = s.strip()
    s = s.replace("\r", "")
    s = s.replace("\t", "")
    s = s.replace("\n", "")
    s = s.replace("  ", " ")
    return s