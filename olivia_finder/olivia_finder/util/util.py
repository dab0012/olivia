import datetime
import multiprocessing

class Util:
    '''
    Utility class with some useful methods uaed in the project
    '''

    # region Strings

    @staticmethod
    def clean_string(string: str):
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

        Examples
        --------
        >>> Util.clean_string("Hello world")
        'Hello world'
        >>> Util.clean_string("Hello world\\n")
        'Hello world'
        >>> Util.clean_string("Hello   world\\n\\n")
        'Hello world'
        '''
        string = string.strip()
        string = string.replace("\r", "")
        string = string.replace("\t", "")
        string = string.replace("\n", "")
        return string.replace("  ", " ")

    '''
    Dictionary with color codes to print styled text to console

    Keys
    ----
    bold : str
        Bold text style
    underline : str
        Underlined text style
    italic : str
        Italic text style
    error : str
        Red color for error messages
    success : str
        Green color for success messages
    warning : str
        Yellow color for warning messages
    info : str
        Blue color for information messages
    end : str
        Reset style
    '''
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
        '2023-03-18_14:40:56'
        '''
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
        4
        """
        # We get the number of cores available in the system
        available_cores = multiprocessing.cpu_count()

        # We calculate the recommended number of threads based on the number of cores
        # available and current state of system resources
        if available_cores > 2:
            return min(available_cores - 1, 2 * int(available_cores ** 0.5))
        else:
            return 1
        