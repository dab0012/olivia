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

import logging
import os
from colorama import Style, Fore

from olivia_finder.config import LoggerConfiguration

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

class UtilLogger:
    '''
    Utility class for logging
    '''

    @staticmethod
    def logg(logger: logging.Logger, text: str, logging_level: str = "NOTSET"):
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

        # Check if the logger is not None
        if logger is None:
            return
        
        # Check if the style is valid
        if logging_level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
            return
        
        # Log the text
        if logging_level == "CRITICAL":
            logger.critical(text)
        elif logging_level == "ERROR":
            logger.error(text)
        elif logging_level == "WARNING":
            logger.warning(text)
        elif logging_level == "INFO":
            logger.info(text)
        elif logging_level == "DEBUG":
            logger.debug(text)
        elif logging_level == "NOTSET":
            logger.log(text)

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

    @staticmethod
    def prepare_loger(filename_tag: str) -> logging.Logger:
        '''
        Prepare the logger

        Returns
        -------
        logging.Logger
            Logger
        '''
        # Make a log file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_timestamp = UtilLogger.get_current_timestamp()
        filename = current_dir + os.sep + "logs" + os.sep + f"{filename_tag}_{current_timestamp}.log"

        # Create logs directory if it does not exist
        if not os.path.exists(current_dir + os.sep + "logs"):
            os.makedirs(current_dir + os.sep + "logs")

        logger_config = LoggerConfiguration(filename = filename, level = logging.DEBUG)
        logger_config.aply_config()

        return logger_config.get_logger()

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




