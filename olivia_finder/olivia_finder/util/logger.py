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
from olivia_finder.util.util import Util
from olivia_finder.util.config_ini import Configuration

class UtilLogger:
    '''
    Utility class for logging
    '''

    STATUS = False

    @staticmethod
    def init_logger(console: bool = True, file: bool = True):
        '''
        Initialize the logger, reading the configuration from config.ini.
        If the configuration is not found, the default values are used.
        
        Parameters
        ----------
        console : bool, optional
            If True, the logger will log to console, by default True
            
        file : bool, optional
            If True, the logger will log to file, by default True
            
        Handles
        -------
        Exception
            If the configuration data is not found, the default values are used.
        '''

        # Get the logging configuration from config.ini
        try:
            logging_format  = Configuration().get_key("logger", "format")
            date_format     = Configuration().get_key("logger", "log_cli_date_format")
            level           = Configuration().get_key("logger", "level")
            filename        = Configuration().get_key("logger", "filename")
            log_path        = Configuration().get_key("folders", "log_dir")
        except Exception:
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

        # Create the file handler
        if file:
            os.makedirs(log_path, exist_ok=True)                # Create the log folder if not exists
            filename = f'{Util.timestamp()}_{filename}'
            fh = logging.FileHandler(f'{log_path}/{filename}')
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
        # Create the console handler
        if console:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        # Set the status to true
        UtilLogger.STATUS = True

    @staticmethod
    def log(text: str):
        '''
        Log the text to the logger if the logger is enabled.

        Parameters
        ----------
        text : str
            The text to log

        '''
        if UtilLogger.STATUS:
            level = logging.getLogger().getEffectiveLevel()
            logging.getLogger().log(level=level, msg=text)                
                
    @staticmethod
    def enable_logger():
        '''
        Enable the logger
        
        Handles
        -------
        Exception
            If the configuration data is not found, the default values are used.
        '''
        UtilLogger.STATUS = True
        logging.disable(logging.NOTSET)

        # Enable configured levels, if not, set to DEBUG
        try:
            level = int(Configuration().get_key("logger", "level"))
        except Exception:
            level = logging.DEBUG

        logging.getLogger().setLevel(level)


    @staticmethod
    def disable_logger():
        '''
        Disable the logger
        '''
        UtilLogger.STATUS = False
        logging.disable(logging.CRITICAL)
