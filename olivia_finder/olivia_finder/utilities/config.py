import configparser
import os
from typing import Optional
from .singleton_decorator import singleton
from .exception import ConfigFileNotFound, ConfigKeyNotFound


@singleton
class Configuration:
    """
    Utility class for obtaining configurations from a config.ini file.
    The config.ini file is read only once and the values are stored in a dictionary.
    The config.ini file path can be changed by passing the path to the constructor.

    .. warning:: It is necessary to initialize the configuration, the most comfortable and global way to do so is through an environment variable

    Attributes
    ----------
    _config : dict
        Configurations read from the config file
    """

    # Class variables
    # ---------------
    _config = {}
    
    def __init__(self, file_path: Optional[str] = None):
        '''
        Initialize the class, read the config file and store the values in a dictionary

        Parameters
        ----------
        file_path : str, optional
            Path to the config file, by default None, 
            in which case the path is read from the environment variable OLIVIA_FINDER_CONFIG_FILE_PATH

        Raises
        ------
        ConfigFileNotFoundError
            If the config file is not found
        '''

        if file_path is None:
            # Read the config file from environment variable
            file_path = os.environ.get('OLIVIA_FINDER_CONFIG_FILE_PATH')

        # Load data from ini file
        config_parser = configparser.ConfigParser()

        try:
            # Read the config file
            with open(f'{file_path}', encoding='utf-8') as f:
                config_parser.read_file(f)

        # If the file is not found, raise an exception
        except FileNotFoundError as e:
            raise ConfigFileNotFound(f'Config file not found in {file_path}') from e
        
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
        ConfigKeyNotFoundError
            If the key is not found in the config file

        '''

        try:
            value = self._config[section][key]
        except KeyError as e:
            raise ConfigKeyNotFound(f'Key {key} not found in section {section}') from e
        
        return value
