'''
File:              config_ini.py
Project:           Olivia-Finder
Created Date:      Thursday March 9th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Thursday March 9th 2023 5:01:30 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
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
    _ini_file = "config.ini"                      # Path to the config file
    _instance = None                              # Singleton instance
    _config = {}                                  # Configurations read from the config file

    def __new__(cls):
        '''
        Singleton pattern
        '''

        if not cls._instance:
            cls._instance = super().__new__(cls)

            # Load data from ini file
            config_parser = configparser.ConfigParser()

            # Get the path of the folder of this file
            parent_folder = os.path.dirname(os.path.dirname(__file__))
            # parent_folder = os.path.dirname(parent_folder)
            
            # file_path = os.path.abspath(__file__)
            # parent_folder = os.path.dirname(os.path.dirname(file_path))

            with open(f'{parent_folder}/{cls._ini_file}') as f:
                config_parser.read_file(f)

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
            raise Exception(f"Key {key} not found in section {section} of config.ini") from e
        
        return value
