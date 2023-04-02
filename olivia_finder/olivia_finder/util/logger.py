import logging
import os
from .util import Util
from .config_ini import Configuration

class MyLogger:
    '''
    Utility class for logging. This class is a singleton

    Attributes
    ----------
    _instance : MyLogger
        Singleton instance of the class
    _status : bool
        Status of the logger. True if enabled, False if disabled
    '''

    _instance = None
    status = False
    level = None
    logger = None

    def __init__(self):
        raise NotImplementedError("Cannot instantiate this class. Use get_instance() instead.")

    @classmethod
    def get_instance(cls):
        '''
        Singleton pattern implementation to create a single instance of the class
        '''
        
        if not cls._instance:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    def _create_instance(cls):
        '''
        Create and configure the logger instance.
        '''
        # Check if the logger is enabled at config.ini
        status = Configuration().get_key("logger", "status")

        if status == "ENABLED":

            # The logger is enabled

            cls.status = True

            # Get the logging configuration from config.ini
            try:
                logging_format  = Configuration().get_key("logger", "format")
                date_format     = Configuration().get_key("logger", "log_cli_date_format")
                level           = Configuration().get_key("logger", "level")
                filename        = Configuration().get_key("logger", "filename")
                log_path        = Configuration().get_key("folders", "log_dir")
            except FileNotFoundError:
                # Fix not found in config.ini
                # Use hardcoded values
                logging_format  = '%(asctime)s - %(levelname)s - %(message)s'
                date_format     = '%Y-%m-%d %H:%M:%S'
                level           = logging.DEBUG
                filename        = "olivia_finder.log"
                log_path        = f'{os.getcwd()}/logs/'

            # Create the logger and configure it

            cls.level = level
            cls.logger = logging.getLogger()
            cls.logger.setLevel(level)
            formatter = logging.Formatter(logging_format, date_format)          

            # Create the file handler
            # Check if file is enabled
            file = Configuration().get_key("logger", "file")
            if file == "ENABLED":
                os.makedirs(log_path, exist_ok=True)                # Create the log folder if not exists
                filename = f'{Util.timestamp()}_{filename}'
                fh = logging.FileHandler(f'{log_path}/{filename}')
                fh.setLevel(level)
                fh.setFormatter(formatter)
                cls.logger.addHandler(fh)
                
            # Create the console handler
            console = Configuration().get_key("logger", "console")
            if console == "ENABLED":
                ch = logging.StreamHandler()
                ch.setLevel(level)
                ch.setFormatter(formatter)
                cls.logger.addHandler(ch)

        else:
            # The logger is disabled

            cls.status = False

        return cls

    @staticmethod
    def log(text: str):
        '''
        Log the text to the logger if the logger is enabled.

        Parameters
        ----------
        text : str
            The text to log

        '''
        _self = MyLogger.get_instance()
        if _self.status:
            # Log the text

            #parse the level string to the corresponding logging level
            if _self.level == "DEBUG":
                _self.level = logging.DEBUG
            elif _self.level == "INFO":
                _self.level = logging.INFO
            elif _self.level == "WARNING":
                _self.level = logging.WARNING
            elif _self.level == "ERROR":
                _self.level = logging.ERROR
            elif _self.level == "CRITICAL":
                _self.level = logging.CRITICAL

            logging.getLogger().log(_self.level, text)
                       
                
    @staticmethod
    def enable_logger():
        '''
        Enable the logger
        
        Handles
        -------
        Exception
            If the configuration data is not found, the default values are used.
        '''
        _self = MyLogger.get_instance()
        _self.status = True

    @staticmethod
    def disable_logger():
        '''
        Disable the logger
        '''
        _self = MyLogger.get_instance()
        _self.status = False
