'''
File:              config.py
Project:           Olivia-Finder
Created Date:      Friday March 3rd 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday March 3rd 2023 7:02:38 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import logging, configparser, os
from olivia_finder.util import UtilLogger

class LoggerConfiguration:
    '''
    Class to configure the logger
    '''

    _instance = None

    def __new__(cls):
        '''
        Constructor of the class
        
        Returns
        -------
        LoggerConfiguration
            LoggerConfiguration object
            
            '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Load data from ini file
            cp = configparser.ConfigParser()

            # Get the logging format
            try:
                cp.read('config.ini')
                logging_format = cp['logger']['format']
                date_format = cp['logger']['date_format']
                level = cp['logger']['level']
                filename = cp['logger']['filename']
                folder = cp['folders']['log_dir']
            except:
                # Fix not found in config.ini
                logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                date_format = '%d-%b-%y %H:%M:%S'
                level = 'DEBUG'
                filename = 'olivia_finder.log'
                folder = 'olivia_finder/logs'

            current_timestamp = UtilLogger.get_current_timestamp()
            filename = f'{folder}{os.sep}{current_timestamp}_{filename}'

            cls._instance.filename = filename
            cls._instance.level = level
            cls._instance.format = logging_format
            cls._instance.date_format = date_format

            logging.basicConfig(
                filename=cls._instance.filename,
                level=logging.getLevelName(cls._instance.level),
                format=cls._instance.format,
                datefmt=cls._instance.date_format
            )

            cls._instance.logger = logging.getLogger(__name__)
            
        return cls._instance

    def get_logger(self) -> logging.Logger:
        '''
        Get the logger

        Returns
        -------
        logging.Logger
            Logger object
        '''
        return self.logger
    
    def get_level(self) -> str:
        '''
        Get the logger level

        Returns
        -------
        str
            Logger level
        '''
        return self.level

    
