import re
from typing import Dict, List

def parse_dependencies(dependencies_str: str) -> List[Dict[str, str]]:
    '''
    Parses the dependencies string and returns a list of dictionaries with the name and version of each dependency
    TODO: A fix is needed to target the version of the dependency, as it's not always well defined

    Parameters
    ----------
    dependencies_str : str
        The dependencies string

    Returns
    -------
    List[Dict[str, str]]
        A list of dictionaries with the name and version of each dependency    
    '''

    # Remove unnecessary line breaks, tabs, and spaces
    pattern = r'\S+\s*(?:\(([^\)]*)\))?'

    # Get names and versions of dependencies
    versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else None for dep in dependencies_str.split(",")]
    names = [re.sub(r'\s*\(.*\)', '', name.strip()) for name in dependencies_str.split(",")]

    # Check if the lists have the same length and are not empty
    if len(names) != len(versions) or not names:
        return []

    return [
        {'name': names[i], 'version': versions[i]} for i in range(len(names))
    ]