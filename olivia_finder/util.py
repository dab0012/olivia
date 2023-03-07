'''
File:              util.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 8:01:57 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import logging, os, configparser    
from colorama import Style, Fore

class Util:
    '''
    Utility class
    '''

    # Colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE

    @staticmethod
    def clean_string(s: str):
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
        '''
        s = s.strip()
        s = s.replace("\r", "")
        s = s.replace("\t", "")
        s = s.replace("\n", "")
        s = s.replace("  ", " ")
        return s

    @staticmethod
    def print_colored(text, color):
        '''
        Print colored text

        Parameters
        ----------
        text : str
            Text to be printed
        color : str
            Color of the text
        '''
        print(color, end="")
        print(text, end="")
        print(Style.RESET_ALL)

    @staticmethod
    def print_styled(text, style):
        '''
        Print text in red

        Parameters
        ----------
        text : str
            Text to be printed
        '''
        if style == "error":
            Util.print_colored(text, Util.RED)
        elif style == "success":
            Util.print_colored(text, Util.GREEN)
        elif style == "warning":
            Util.print_colored(text, Util.YELLOW)
        elif style == "info":
            Util.print_colored(text, Util.BLUE)
        elif style == "title":
            Util.print_colored(text, Util.BLUE)
            print(Style.UNDERLINE)
        elif style == "subtitle":
            Util.print_colored(text, Util.BLUE)
            print(Style.BRIGHT)

'''
Logger utility class
'''
class UtilLogger:
    '''
    Utility class for logging
    '''

    @staticmethod
    def logg(text: str):
        '''
        Log a text

        Parameters
        ----------
        logger : logging.Logger
            Logger to use
        text : str
            Text to log
        logging_level : str, optional
            Logging level, by default "NOTSET"
        '''

        logger = LoggerConfiguration().get_logger()
        level = LoggerConfiguration().get_level()
        
        # Check if the style is valid
        if level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            return
        
        # Log the text
        if level == "CRITICAL":
            logger.critical(text)
        elif level == "ERROR":
            logger.error(text)
        elif level == "WARNING":
            logger.warning(text)
        elif level == "INFO":
            logger.info(text)
        elif level == "DEBUG":
            logger.debug(text)

    @staticmethod
    def get_current_timestamp():
        '''
        Get the current timestamp

        Returns
        -------
        str
            Current timestamp
        '''
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            except:
                # Fix not found in config.ini
                logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                date_format = '%d-%b-%y %H:%M:%S'
                level = 'DEBUG'
                filename = 'olivia_finder.log'

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

            # Get loger folder from config.ini
            log_dir = UtilConfig.get_value_config_file("folders", "log_dir")

            # Make directory if it does not exist
            os.makedirs(log_dir, exist_ok=True)
            
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
        Get the logging level

        Returns
        -------
        str
            Logging level
        '''
        return self.level

'''
Multithreading utility class
'''
class UtilMultiThreading:
    """
    Utility class for multithreading
    """

    @staticmethod
    def recommended_threads():
        """
        Gets the recommended number of threads to use.
        """
        # We get the number of cores available in the system
        import multiprocessing
        available_cores = multiprocessing.cpu_count()

        # We calculate the recommended number of threads based on the number of cores
        # available and current state of system resources
        if available_cores > 2:
            return min(available_cores - 1, 2 * int(available_cores ** 0.5))
        else:
            return 1

'''
Config utility class
'''
class UtilConfig:

    INI_FILE = "olivia_finder/config.ini"

    @staticmethod
    def get_value_config_file(section:str, key: str):
        """
        Get a value from a config file

        Parameters
        ----------
        section : str
            Section of the config file
        key : str
            Key of the config file
    
        Returns
        -------
        str
            Value of the key
        """
        import configparser
        config = configparser.ConfigParser()
        config.read(UtilConfig.INI_FILE)
        return config[section][key]


