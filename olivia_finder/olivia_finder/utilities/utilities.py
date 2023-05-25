import os


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

def setup_path(path: str) -> None:
    '''
    Setup a path, creating the directory if it does not exist

    Parameters
    ----------
    path : str
        Path to be setup

    Returns
    -------
    str
        Setup path

    Examples
    --------
    >>> Util.setup_path("test")
    'test'
    '''

    file_name = os.path.basename(path)
    path = path.replace(file_name, "")

    if not os.path.exists(path) and path != "":
        os.makedirs(path)