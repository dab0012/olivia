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

class Util:
    '''
    Utility class
    '''

    # Colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE

    @staticmethod
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

    @staticmethod
    def print_colored(text, color):
        '''
        Print colored text

        Parameters
        ----------
        text : str
            Text to be printed
        color : str
            Color of the text
        '''
        print(color, end="")
        print(text, end="")
        print(Style.RESET_ALL)

    @staticmethod
    def print_styled(text, style):
        '''
        Print text in red

        Parameters
        ----------
        text : str
            Text to be printed
        '''
        if style == "error":
            Util.print_colored(text, Util.RED)
        elif style == "success":
            Util.print_colored(text, Util.GREEN)
        elif style == "warning":
            Util.print_colored(text, Util.YELLOW)
        elif style == "info":
            Util.print_colored(text, Util.BLUE)
        elif style == "title":
            Util.print_colored(text, Util.BLUE)
            print(Style.UNDERLINE)
        elif style == "subtitle":
            Util.print_colored(text, Util.BLUE)
            print(Style.BRIGHT)

        

