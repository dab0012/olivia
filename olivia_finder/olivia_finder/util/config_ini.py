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

class Configuration:
    """
    Utility class for config.ini
    """

    # Class variables
    # ---------------
    _ini_file = "./config.ini"        # Path to the config file
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
            with open(cls._ini_file) as f:
                config_parser.read_file(f)
            cls._config = dict(config_parser)
        
        return cls._instance

    def get_key(self, section:str, key: str):
        '''
        Get a value from the config file
        
        ---
        Parameters
        -   section: str -> Section of the config file
        -   key: str -> Key of the config file

        ---
        Returns
        -   str -> Value of the key, or None if not found
        '''

        return self._config[section][key]
