import configparser
import os
from singleton_decorator import singleton
@singleton
class Configuration:
    """
    Utility class for config.ini file
    This class is a singleton, so it can be used as a global variable.
    The config.ini file must be in the same folder as this file.    

    Attributes
    ----------
    _ini_file : str
        Path to the config file  
    _instance : Configuration
        Singleton instance
    _config : dict
        Configurations read from the config file
    """

    # Class variables
    # ---------------
    _DEFAULT_CONF_PATH = "../config.ini"          # Path to the config file
    _config = {}                                  # Configurations read from the config file
    
    def __init__(self, file_path: str = _DEFAULT_CONF_PATH):
        '''
        Initialize the class
        '''

        # Load data from ini file
        config_parser = configparser.ConfigParser()

        # Get the path of the folder of this file
        parent_folder = os.path.dirname(os.path.dirname(__file__))

        try:
            # Read the config file
            with open(f'{parent_folder}/{file_path}', encoding='utf-8') as f:
                config_parser.read_file(f)

        # If the file is not found, raise an exception
        except FileNotFoundError as e:
            raise FileNotFoundError(f'Config file not found in {parent_folder}') from e
        
        self._config = dict(config_parser)

    def get_key(self, section:str, key: str):
        '''
        Get a value from the config file by section and key

        Parameters
        ----------
        section : str
            Section of the config file
        key : str
            Key of the config file

        Returns
        -------
        str
            Value of the key in the section
        
        Raises
        ------
        keyError
            If the key is not found in the section            
        '''

        try:
            value = self._config[section][key]
        except KeyError as e:
            raise KeyError(f'Key {key} not found in section {section}') from e
        
        return value
