'''
File:              util.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 8:01:57 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

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