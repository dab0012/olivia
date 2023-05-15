import datetime
import logging
import os
from .config import Configuration
from singleton_decorator import singleton

@singleton
class MyLogger:
    '''
    Custom logger class that implements singleton pattern
    to ensure that only one instance of the logger is created
    The logger configuration is read from config.ini

    Attributes
    ----------
    logger : logging.Logger
        The logger instance
    level : logging.level
        The logging level
    '''

    def __init__(self):
        '''
        Initialize the logger with the configuration from config.ini
        '''
        self.__logger = None
        self.__level = None
        self.__configure_logger()

    def __configure_logger(self):
        '''
        Create and configure the logger instance
        The logger configuration is read from config.ini
        '''
        # Get the logging configuration from config.ini
        try:
            logging_format  = Configuration().get_key("logger", "format")
            date_format     = Configuration().get_key("logger", "log_cli_date_format")
            level           = Configuration().get_key("logger", "level")
            filename        = Configuration().get_key("logger", "filename")
            log_path        = Configuration().get_key("folders", "log_dir")
            file            = Configuration().get_key("logger", "file")
            console         = Configuration().get_key("logger", "console")

        except FileNotFoundError:
            # Fix not found in config.ini
            # Use hardcoded values
            logging_format, date_format, level, log_path, file, console = self.__load_defaut_config()

        # Set the logging level
        self.__level = level.upper()

        # Create the logger and configure it
        self.__logger = logging.getLogger()
        self.__logger.setLevel(self.__level)
        formatter = logging.Formatter(logging_format, date_format)

        # Create the file handler
        if file == "ENABLED":
            os.makedirs(log_path, exist_ok=True)                # Create the log folder if not exists
            filename = f'{self.__timestamp()}_{filename}'
            fh = logging.FileHandler(f'{log_path}/{filename}')
            fh.setLevel(self.__level)
            fh.setFormatter(formatter)
            self.__logger.addHandler(fh)

        # Create the console handler
        if console == "ENABLED":
            ch = logging.StreamHandler()
            ch.setLevel(self.__level)
            ch.setFormatter(ConsoleFormatter())
            self.__logger.addHandler(ch)

    def __load_defaut_config(self):
        '''
        Load the default configuration for the logger
        '''

        logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        level = logging.DEBUG
        log_path = 'logs'
        file = "ENABLED"
        console = "ENABLED"
        return logging_format,date_format,level,log_path,file,console

    def get_logger(self) -> logging.Logger:
        '''
        Returns the logger instance

        Returns
        -------
        logging.Logger
            The logger instance
        '''
        return self.__logger
    
    def enable(self):
        '''
        Enable the logger
        '''
        self.__logger.disabled = False

    def disable(self):
        '''
        Disable the logger
        '''
        self.__logger.disabled = True

    def disable_all_loggers(self):
        '''
        Disable all loggers
        '''
        logging.disable(logging.CRITICAL)

    def enable_all_loggers(self):
        '''
        Enable all loggers
        '''
        logging.disable(logging.NOTSET)

    def set_level(self, level):
        '''
        Set the logging level

        Parameters
        ----------
        level : str
            The logging level
        '''
        self.__level = level.upper()
        self.__logger.setLevel(self.__level)

        # Set the level for all handlers
        for handler in self.__logger.handlers:
            handler.setLevel(self.__level)
            

    def __timestamp(self):
        '''
        Get the current timestamp

        Returns
        -------
        str
            Current timestamp

        Examples
        --------
        >>> Util.timestamp()
        '2023-03-18_14:40:56'
        '''
        return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
class ConsoleFormatter(logging.Formatter):
    '''
    Custom formatter class that implements the ANSI escape sequences
    to color the log messages based on the logging level
    '''

    GREEN = "\x1b[32;20m"
    BLUE = "\x1b[34;20m"
    YELLOW = "\x1b[33;20m"
    ORANGE = "\x1b[38;5;208;20m"
    RED = "\x1b[31;20m"
    RESET = "\x1b[0m"
    DEFAULT_FORMAT_PRE = "%(asctime)s [%(levelname)s] in %(module)s.%(funcName)s (%(filename)s:%(lineno)d)"
    DEFAULT_FORMAT_END = "\n%(message)s"


    FORMATS = {
        logging.DEBUG: GREEN + DEFAULT_FORMAT_PRE + RESET + DEFAULT_FORMAT_END,
        logging.INFO: BLUE + DEFAULT_FORMAT_PRE + RESET + DEFAULT_FORMAT_END,
        logging.WARNING: YELLOW + DEFAULT_FORMAT_PRE + RESET + DEFAULT_FORMAT_END,
        logging.ERROR: ORANGE + DEFAULT_FORMAT_PRE + RESET + DEFAULT_FORMAT_END,
        logging.CRITICAL: RED + DEFAULT_FORMAT_PRE + RESET + DEFAULT_FORMAT_END,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)