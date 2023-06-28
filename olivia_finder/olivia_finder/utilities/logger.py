from __future__ import annotations
import logging
from typing import Optional
from .config import Configuration
from .exception import OliviaFinderException
from .utilities import setup_path

class MyLogger:
    
    @staticmethod
    def configure(config_key: str) -> logging.Logger:
        '''
        Initializes the logger

        Parameters
        ----------
        config_key : str
            Key of the configuration file that contains the logger configuration

        Returns
        -------
        logging.Logger
            Logger with the given name
        '''

        logger_name = Configuration().get_key(config_key, 'name')

        # Check if the logger has already been initialized
        if logger_name in logging.Logger.manager.loggerDict:
            
            MyLogger.get_logger(logger_name).warning(
                f"The logger with name {logger_name} has already been initialized"
            )
            return MyLogger.get_logger(logger_name)

        # We get the logger
        logger = logging.getLogger(logger_name)
        
        # Check if the logger has file handler
        if Configuration().get_key(config_key, 'file_handler').upper() == 'ENABLED':

            # Folder where the log files will be stored
            log_folder = Configuration().get_key('folders', 'logger')
            setup_path(log_folder)

            # We enable the file
            MyLogger.enable_file(
                logger_name=logger_name,
                log_file=f'{log_folder}/{logger_name}.log',
                log_file_level=Configuration().get_key(config_key, 'level')
            )
      
        # Check if the logger has console handler
        if Configuration().get_key(config_key, 'console_handler').upper() == 'ENABLED':
            # We enable the console
            MyLogger.enable_console(
                logger_name=logger_name,
                console_level=Configuration().get_key(config_key, 'level')
            )

        # Disable if configured
        olivia_finder_logger_name = Configuration().get_key('olivia_finder_logger', 'name')
        if Configuration().get_key('olivia_finder_logger', 'status').upper() == 'DISABLED':
            MyLogger().get_logger().disabled = True
            MyLogger().get_logger(olivia_finder_logger_name).disabled = True
            logger.disabled = True
        elif Configuration().get_key(config_key, 'status').upper() == 'DISABLED':
            logger.disabled = True


        # Dissable propagation 
        logger.propagate = False

        return logger
    
    @staticmethod
    def get_logger(logger_name: Optional[str] = None) -> logging.Logger:
        '''
        Returns the logger with the given name

        Parameters
        ----------
        logger_name : str
            Name of the logger to return

        Returns
        -------
        logging.Logger
            Logger with the given name
        '''
        
        if logger_name is None:
            return logging.getLogger()

        # Check if the logger has already been initialized
        if logger_name not in logging.Logger.manager.loggerDict:
            try:
                MyLogger.configure(logger_name)
                logging.getLogger(logger_name).propagate = False
            except OliviaFinderException:
                return logging.getLogger()

        return logging.getLogger(logger_name)

    @staticmethod
    def enable_console(logger_name: str, console_level: str) -> None:
        """
        Enables the console

        Parameters
        ----------
        logger_name : str
            Name of the logger to enable the console for.
        
        console_level : str
            Log level to configure.

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> MyLogger.enable_console()

        """
        
        # The handler is created for the console
        h = logging.StreamHandler()
        h.setLevel(console_level.upper())
        h.setFormatter(ConsoleLogFormatter())

        # The handler is added to the logger
        logging.getLogger(logger_name).addHandler(h)

        # set the level of the logger (Must be the same as the handler)
        logging.getLogger(logger_name).setLevel(console_level.upper())

    @staticmethod
    def enable_file(logger_name: str, log_file: str, log_file_level: str) -> None:
        """
        Enables the file

        Parameters
        ----------
        logger_name : str
            Name of the logger to enable the file for.

        log_file : str
            Name of the file to store the logs in.

        log_file_level : str
            Log level to configure.

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> MyLogger.enable_file()
        """
        
        # The handler is created for the file
        h = logging.FileHandler(log_file)
        h.setLevel(log_file_level.upper())
        h.setFormatter(FileLogFormatter())


        # The handler is added to the logger
        logging.getLogger(logger_name).addHandler(h)
        # set the level of the logger (Must be the same as the handler)
        logging.getLogger(logger_name).setLevel(log_file_level.upper())

    @staticmethod
    def configure_level(logger_name: str, handler_type: str, level: str) -> None:
        """
        Description
        -----------
        Configures the log level for the handler of a logger given its name and type.
        
        Parameters
        ----------
        logger_name : str
            Name of the logger to configure the level for.
            
        handler_type : str
            Type of handler to configure.
            
        level : str
            Log level to configure.
            
    .. note::
        Valid handler types are: 
        -   ``console`` for the console handler
        -   ``file`` for the file handler
        -   ``all`` for both handlers
        -   ``global`` for all handlers of all loggers
        
        Valid log levels are:
        -   ``DEBUG`` for debugging messages
        -   ``INFO`` for informational messages
        -   ``WARNING`` for warning messages
        -   ``ERROR`` for error messages
        -   ``CRITICAL`` for critical messages
        -   ``NOTSET`` for messages without level
                                
        Raises
        ------
        NotImplementedError
            If the specified handler type is not valid
            If the specified log level is not valid
                
        Examples
        --------
        >>> from my_logger import MyLogger
        >>> logger = MyLogger.logger()
        >>> logger.configure_level("console", "DEBUG")
        >>> logger.configure_level("file", "DEBUG")
        """
        
        logger = logging.getLogger(logger_name)
        handler_list = []
        # Validate the handler type
        if handler_type == "console":
            handler_list.append(logger.handlers[0])
        elif handler_type == "file":
            handler_list.append(logger.handlers[1])
        elif handler_type == "all":
            handler_list = logger.handlers
        elif handler_type == "global":
            handler_list = logging.root.handlers
        else:
            raise NotImplementedError(
                "The specified handler type is not valid",
                "\n",
                "Valid handler types are: 'console', 'file', 'all', 'global'",
            )

        for handler in handler_list:

            # Validate the log level
            if level.upper() == "DEBUG":
                handler.setLevel(logging.DEBUG)
            elif level.upper() == "INFO":
                handler.setLevel(logging.INFO)
            elif level.upper() == "WARNING":
                handler.setLevel(logging.WARNING)
            elif level.upper() == "ERROR":
                handler.setLevel(logging.ERROR)
            elif level.upper() == "CRITICAL":
                handler.setLevel(logging.CRITICAL)
            elif level.upper() == "NOTSET":
                handler.setLevel(logging.NOTSET)
            else:
                raise NotImplementedError(
                    "The specified log level is not valid",
                    "\n",
                    "Valid log levels are: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET'",
                )
        
        # Set the level of the logger
        logger.setLevel(level.upper())

class ConsoleLogFormatter(logging.Formatter):
    """
    Description
    -----------
    Custom formatter for console log messages.

    Examples
    --------
    >>> from my_logger import MyLogger
    >>> logger = MyLogger.logger()
    >>> logger.configure_formatter("console", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    """

    __COLOR_GREEN = "\x1b[32;20m"
    __COLOR_BLUE = "\x1b[34;20m"
    __COLOR_YELLOW = "\x1b[33;20m"
    __COLOR_ORANGE = "\x1b[38;5;208;20m"
    __COLOR_RED = "\x1b[31;20m"
    __COLOR_RESET = "\x1b[0m"
    
    # Formato de la cabecera del log
    # Tiempo [nombre_logger(Nivel)] -> Archivo:Linea
    __FORMAT_HEADER = "%(asctime)s [%(name)s(%(levelname)s)] -> %(filename)s:%(lineno)d"
    __FORMAT_MESSAGE = "\n%(message)s"

    __FORMATS = {
        logging.DEBUG: __COLOR_GREEN + __FORMAT_HEADER + __COLOR_RESET + __FORMAT_MESSAGE,
        logging.INFO: __COLOR_BLUE + __FORMAT_HEADER + __COLOR_RESET + __FORMAT_MESSAGE,
        logging.WARNING: __COLOR_YELLOW + __FORMAT_HEADER + __COLOR_RESET + __FORMAT_MESSAGE,
        logging.ERROR: __COLOR_ORANGE + __FORMAT_HEADER + __COLOR_RESET + __FORMAT_MESSAGE,
        logging.CRITICAL: __COLOR_RED + __FORMAT_HEADER + __COLOR_RESET + __FORMAT_MESSAGE,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Description
        -----------
        Formats the log message

        Parameters
        ----------
        record : logging.LogRecord
            Log message to format
            
        Returns
        -------
        str
            Formatted log message

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> logger = MyLogger.logger()
        >>> logger.configure_formatter("console", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        """
        
        log_fmt = self.__FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class FileLogFormatter(logging.Formatter):
    """
    Description
    -----------
    
    Custom formatter for file log messages.
    """

    __DEFAULT_FORMAT = "%(asctime)s [%(name)s(%(levelname)s)] -> %(filename)s:%(lineno)d\n%(message)s"

    def format(self, record: logging.LogRecord) -> str:
        """
        Description
        -----------
        Formats the log message

        Parameters
        ----------
        record : logging.LogRecord
            Log message to format

        Returns
        -------
        str
            Formatted log message

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> logger = MyLogger.logger()
        >>> logger.configure_formatter("file", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        """
        
        formatter = logging.Formatter(self.__DEFAULT_FORMAT)
        return formatter.format(record)
    
