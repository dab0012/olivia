'''
File:              logger.py
Project:           Olivia-Finder
Created Date:      Thursday March 9th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Thursday March 9th 2023 4:43:24 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import logging, os

from .config_ini import Configuration
from .util import Util

class UtilLogger:
    '''
    Utility class for logging
    '''

    STATUS = False

    @staticmethod
    def init_logger():
        '''
        Initialize the logger
        '''

        # Get the logging configuration from config.ini
        try:
            logging_format  = Configuration().get_key("logger", "format")
            date_format     = Configuration().get_key("logger", "log_cli_date_format")
            level           = Configuration().get_key("logger", "level")
            filename        = Configuration().get_key("logger", "filename")
            log_path        = Configuration().get_key("folders", "log_dir")
        except:
            # Fix not found in config.ini
            logging_format  = '%(asctime)s - %(levelname)s - %(message)s'
            date_format     = '%Y-%m-%d %H:%M:%S'
            level           = logging.DEBUG
            filename        = "olivia_finder.log"
            log_path        = f'{os.getcwd()}/logs/'

        # Create the logger and configure it
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(logging_format, date_format)          
        
        # Create the log directory if it does not exist
        os.makedirs(log_path, exist_ok=True)
 
        # Create the file handler
        filename = f'{Util.timestamp()}_{filename}'
        fh = logging.FileHandler(f'{log_path}/{filename}')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Create the console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Set the status to true
        UtilLogger.STATUS = True

    @staticmethod
    def log(text: str):
        '''
        Log a text

        ---
        Parameters
        -   text: str -> Text to be logged
        '''
        if UtilLogger.STATUS:
            
            logger = logging.getLogger()

            # Log the text
            logger.log(logging.INFO, text)

    @staticmethod
    def enable_logger():
        '''
        Enable the logger
        '''
        UtilLogger.STATUS = True
        logging.disable(logging.NOTSET)

        # Enable configured levels, if not, set to DEBUG
        logger = logging.getLogger()
        try:
            level = Configuration().get_key("logger", "level")
        except:
            level = logging.DEBUG

        logger.setLevel(level)


    @staticmethod
    def disable_logger():
        '''
        Disable the logger
        '''
        UtilLogger.STATUS = False
        logging.disable(logging.CRITICAL)
