'''
config_ini.py
=============

Description
-----------

Module that contains ...

File information:
    - File: config_ini.py
    - Project: util
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

import configparser
import os

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
    _ini_file = "../config.ini"                      # Path to the config file
    _instance = None                              # Singleton instance
    _config = {}                                  # Configurations read from the config file

    def __new__(cls):
        '''
        Singleton pattern implementation to create a single instance of the class
        '''

        if not cls._instance:
            cls._instance = super().__new__(cls)

            # Load data from ini file
            config_parser = configparser.ConfigParser()

            # Get the path of the folder of this file
            parent_folder = os.path.dirname(os.path.dirname(__file__))

            try:
                # Read the config file
                with open(f'{parent_folder}/{cls._ini_file}', encoding='utf-8') as f:
                    config_parser.read_file(f)

            # If the file is not found, raise an exception
            except FileNotFoundError as e:
                raise FileNotFoundError(f'Config file not found in {parent_folder}') from e

            cls._config = dict(config_parser)
        
        return cls._instance

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
