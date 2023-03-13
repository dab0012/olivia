'''
File:              util.py
Project:           Olivia-Finder
Created Date:      Thursday March 9th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Thursday March 9th 2023 4:47:21 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

class Util:
    '''
    Utility class with some useful methods
    '''

    # region Strings

    @staticmethod
    def clean_string(s: str):
        '''
        Clean a string from whitespaces and newlines

        Parameters
        ----------
        s : str
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
        return s.replace("  ", " ")

    # A dictionary with some ANSI color codes
    STYLES = {
        "bold": "\033[1m",
        "underline": "\033[4m",
        "italic": "\033[3m",
        "error": "\033[91m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "info": "\033[94m",
        "end": "\033[0m"
    }

    @staticmethod
    def print_colored(text: str, color: str):
        '''
        Print colored text
        Color must be a Fore.*** constant or a ANSI color code

        Parameters
        ----------
        text : str
            Text to be printed
        color : str
            Color of the text

        Raises
        ------
        ValueError
            If the color is not valid

        Examples
        --------
        >>> Util.print_colored("Hello world", Fore.RED)
        >>> Util.print_colored("Hello world", "\033[91m")
        '''

        print(color, end="")
        print(text, end="")
        print(Util.STYLES["end"])

    @staticmethod
    def print_styled(text, style):
        '''
        Print text with a style:
        Supported styles:
        -   [bold, underline, italic, error, success, warning, info]

        Parameters
        ----------
        text : str
            Text to be printed
        style : str
            Style of the text

        Raises
        ------
        ValueError
            If the style is not valid
        
        Examples
        --------
        >>> Util.print_styled("Hello world", "bold")
        >>> Util.print_styled("Hello world", "underline")
        >>> Util.print_styled("Hello world", "italic")
        '''

        # Check if the style is valid
        if style not in Util.STYLES:
            raise ValueError("Invalid style")

        print(Util.STYLES[style], end="")
        print(text, end="")
        print(Util.STYLES["end"])
        
    # endregion

    @staticmethod
    def timestamp():
        '''
        Get the current timestamp

        Returns
        -------
        str
            Current timestamp

        Examples
        --------
        >>> Util.timestamp()
        '''
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    @staticmethod
    def recommended_threads():
        """
        Gets the recommended number of threads to use.

        Returns
        -------
        int
            The recommended number of threads to use
        
        Examples
        --------
        >>> Util.recommended_threads()
        """
        # We get the number of cores available in the system
        import multiprocessing
        available_cores = multiprocessing.cpu_count()

        # We calculate the recommended number of threads based on the number of cores
        # available and current state of system resources
        if available_cores > 2:
            return min(available_cores - 1, 2 * int(available_cores ** 0.5))
        else:
            return 1

