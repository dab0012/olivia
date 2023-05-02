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
dictionary with color codes to print styled text to console

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
    print(STYLES["end"])

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
    if style not in STYLES:
        raise ValueError("Invalid style")

    print(STYLES[style], end="")
    print(text, end="")
    print(STYLES["end"])
 
