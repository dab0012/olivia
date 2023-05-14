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
