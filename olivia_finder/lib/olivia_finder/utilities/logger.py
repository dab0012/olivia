from __future__ import annotations
import logging
import os
from typing import Optional

class MyLogger:
    
    """
    This module defines a custom logger class, MyLogger, that can be used to configure and obtain customized instances of loggers using Python's logging module. It provides methods to configure the log format and level, as well as to remove old log files.

    Classes
    -------
    MyLogger
        The main class that implements the custom logger.

    ConsoleLogFormatter
        Custom formatter for log messages on the console.

    FileLogFormatter
        Custom formatter for log messages in a file.

    Methods
    -------
    MyLogger.get_logger(logger_name, log_level='DEBUG', enable_console=True, console_level='DEBUG', log_file='MyLogger.log', log_file_level='DEBUG', clear_old_files=False)
        Static method to obtain an instance of the logging.Logger class with the specified configuration.

    MyLogger.configure_formatter(logger, handler, formatter)
        Static method to configure the log message format for a specific logger and handler type.

    MyLogger.configure_level(logger, handler, level)
        Static method to configure the log level for a specific logger and handler type.

    MyLogger.clear_old_log_files(log_file, days_to_keep)
        Static method to remove old log files.

    Attributes
    ----------
    MyLogger.__instances : dict[str, MyLogger]
        A dictionary that stores instances of the class.

    MyLogger.DEFAULT_NAME : str
        The default logger name.

    MyLogger.DEFAULT_LEVEL : str
        The default log level.

    MyLogger.DEFAULT_USE_CONSOLE : bool
        A boolean flag indicating whether console output is enabled.

    MyLogger.DEFAULT_LOG_FILE : str
        The default log file name.


    """


    __instances: dict[str, MyLogger] = None   # type: ignore

    # Configuración del logger
    # -----------------------
    DEFAULT_NAME = "MyLogger"  # Nombre del logger
    DEFAULT_LEVEL = "DEBUG"  # Nivel de log
    DEFAULT_USE_CONSOLE = True  # Habilitar consola
    DEFAULT_LOG_FILE = "MyLogger.log"  # Nombre del archivo de log
    
    @staticmethod
    def get_logger( 
        logger_name: Optional[str] = None,
        log_level: str = DEFAULT_LEVEL, 
        enable_console: bool = DEFAULT_USE_CONSOLE, 
        console_level: str = DEFAULT_LEVEL, 
        log_file: str = DEFAULT_LOG_FILE, 
        log_file_level: str = DEFAULT_LEVEL, 
        clear_old_files: bool = False,
        set_default: bool = False
    ) -> logging.Logger:
        """
        Description
        -----------
        
        Static method to obtain an instance of the ``logging.Logger`` class with the specified configuration.
        
    .. note::
        This function is designed to be used as a **constructor** of the ``MyLogger`` class instance, 
        which is responsible for configuring the logger with the user-specified configuration.
        
        **As this class implements the Singleton design pattern, only the configuration specified in the first call to this method will have an effect. In subsequent calls, the class instance with the configuration specified in the first call will be returned.**
                
    .. warning::
        If this method is called without specifying configuration, the **default configuration** will be applied:
        
        -    ``DEFAULT_NAME = "MyLogger"  # Logger name``
        -    ``DEFAULT_LEVEL = "DEBUG"  # Log level``
        -    ``DEFAULT_USE_CONSOLE = True  # Enable console``
        -    ``DEFAULT_LOG_FILE = "MyLogger.log"  # Log file name``
        
        Parameters
        ----------
        logger_name : str, optional
            Logger name, default 'MyLogger'
        log_level : str, optional
            Log level, default 'DEBUG'
        enable_console : bool, optional
            Enable console, default True
        log_file : str, optional
            Log file name, default 'MyLogger.log'
        clear_old_files : bool, optional
            Remove old log files, default False
            If a log file name is specified, the specified file will be removed
            If no log file name is specified, all log files in the current directory will be removed  
                       
        Returns
        -------
        logging.Logger
            Object of the logging.Logger class with the specified configuration
                
        Raises
        ------
        NotImplementedError
            If an attempt is made to instantiate the class directly
                
        Examples
        --------
        >>> from my_logger import MyLogger
        ...
        >>> MyLogger.get_logger(
        ...     name="L1", log_level="debug", enable_console=True,
        ...     log_file="L1.log", clear_previous_log=True
        ... ).debug("Logger L1 initialized")
        ...
        >>> MyLogger.get_logger("L1").debug("Logger L1 doing something")
        ...
        >>> # The logger configuration can be omitted to use the default configuration
        >>> # If "L2" already exists, the class instance with the configuration specified in the first call will be returned
        >>> # If "L2" does not exist, a new class instance with the default configuration will be created
        >>> MyLogger.get_logger("L2").debug("Test message")
        
        """
        
        # If there is no logger name, the default logger is returned or an exception is raised
        if logger_name is None and MyLogger.__instances.keys().__contains__("DEFAULT"):
            return MyLogger.__instances["DEFAULT"].__logger
        elif logger_name is None and MyLogger.__instances.keys().__contains__("DEFAULT") is False:
            raise Exception("No default logger has been created")
        
        # Store the instances of the class in a dictionary
        if MyLogger.__instances is None:
            MyLogger.__instances = {}

        # If the logger name is not in the dictionary, create a new instance of the class
        # Otherwise, return the instance of the class with the specified name
        if MyLogger.__instances.keys().__contains__(logger_name):
            # Set the default logger
            if set_default:
                MyLogger.__instances["DEFAULT"] = MyLogger.__instances[logger_name] # type: ignore
                
            return MyLogger.__instances[logger_name].__logger  # type: ignore
        else:
            

            MyLogger(
                name=logger_name,
                log_level=log_level,
                enable_console=enable_console,
                console_level=console_level,
                log_file=log_file,
                log_file_level=log_file_level
            )

            # Eliminar los archivos de log antiguos
            if clear_old_files:
                MyLogger.clear_old_log_files(logger_name) # type: ignore
                

            # Set the default logger
            if set_default:
                MyLogger.__instances["DEFAULT"] = MyLogger.__instances[logger_name] # type: ignore
        
            return MyLogger.__instances[logger_name].__logger # type: ignore

    def __init__(self, 
        name: Optional[str], 
        log_level: str,
        enable_console: bool,
        console_level: str,
        log_file: str,
        log_file_level: str
    ):
        """
        **Class constructor**
        
        .. danger::
            **This class is designed to be instantiated from the static method ``get_logger()``**
        
        Raises
        ------
            NotImplementedError
                If an attempt is made to instantiate the class directly
        """

        if MyLogger.__instances.keys().__contains__(name):
            raise NotImplementedError(
                "This class is designed to be instantiated from the static method 'get_logger()'.\n"
                "If you want to change the configuration of the logger, you must call the static method 'get_logger()' with the new configuration."
            )

        MyLogger.__instances[name] = self # type: ignore

        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(log_level.upper())
        self.__file = log_file

        # The handler is created for the console
        if enable_console:
            self.__console_handler = logging.StreamHandler()
            self.__console_handler.setLevel(console_level.upper())
            self.__console_handler.setFormatter(ConsoleLogFormatter())
            self.__logger.addHandler(self.__console_handler)

        #The handler is created for the file
        if log_file is not None:
            self.__file_handler = logging.FileHandler(log_file)
            self.__file_handler.setLevel(log_file_level.upper())
            self.__file_handler.setFormatter(FileLogFormatter())
            self.__logger.addHandler(self.__file_handler)


    @staticmethod
    def enable_console(logger_name: str, console_level: str) -> None:
        """
        Enables the console

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
        MyLogger.__instances[logger_name].__logger.addHandler(h)

        # set the level of the logger (Must be the same as the handler)
        MyLogger.__instances[logger_name].__logger.setLevel(console_level.upper())

    
    @staticmethod
    def disable_console(logger_name: str) -> None:
        """
        Disables the console

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> MyLogger.disable_console()
        """
        
        # Get the logger
        logger = MyLogger.get_logger(logger_name)
        
        # The handler is removed from the logger
        logger.removeHandler(
            MyLogger.__instances[logger_name].__console_handler
        )
        


    @staticmethod
    def enable_file(logger_name: str, log_file: str, log_file_level: str) -> None:
        """
        Enables the file

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
        MyLogger.__instances[logger_name].__logger.addHandler(h)

        # set the level of the logger (Must be the same as the handler)
        MyLogger.__instances[logger_name].__logger.setLevel(log_file_level.upper())

    
    @staticmethod
    def disable_file(logger_name: str) -> None:
        """
        Disables the file

        Examples
        --------
        >>> from my_logger import MyLogger
        >>> MyLogger.disable_file()
        """
        
        # Get the logger
        logger = MyLogger.get_logger(logger_name)
        
        # The handler is removed from the logger
        logger.removeHandler(
            MyLogger.__instances[logger_name].__file_handler
        )

          
    @staticmethod
    def clear_old_log_files(logger_name: Optional[str]) -> None:
        """
        Description
        -----------
        Deletes old log files:
        
        - Deletes all .log files in the current directory
        - Deletes the current log file configured in the class

        Examples
        --------
        >>> from my_logger import MyLogger # Import the class
        >>> MyLogger.clear_old_log_files() # Delete old log files
        """
        
        # Delete all .log files in the current directory
        for file in os.listdir():
            if file.endswith(".log"):
                os.remove(file)
                
        # Delete the default log file
        if os.path.exists(MyLogger.DEFAULT_LOG_FILE):
            os.remove(MyLogger.DEFAULT_LOG_FILE)

        if logger_name is not None and \
            MyLogger.__instances.keys().__contains__(logger_name) and \
            MyLogger.__instances[logger_name].__file is not None:

            if os.path.exists(MyLogger.__instances[logger_name].__file):
                os.remove(MyLogger.__instances[logger_name].__file)    

                # Create an empty file
                os.mknod(MyLogger.__instances[logger_name].__file)

    @staticmethod
    def configure_formatter(logger_name: str, handler_type: str, format: str) -> None:
        """
        Description
        -----------
        
        Configures the log message format for the handler of a logger given its name and type.
        
        Parameters
        ----------
            logger_name : str
                Name of the logger to configure the format for.
                
            handler_type : str
                Type of handler to configure.
                
            format : str
                Format of the log messages. Any valid format of the logging.Formatter class can be used.
                
        .. note::
            Valid handler types are: `console`, `file`, `all`
            
        Examples
        --------
        >>> # Configure the log message format for the console handler
        >>> MyLogger.configure_formatter(
        ...     logger_name="logger_1",
        ...     handler_type="console",
        ...     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ... ) 
        """
        
        if logger_name is None:
            raise ValueError("The logger name cannot be None")
        
        instance = MyLogger.__instances[logger_name]

        if instance is None:
            raise ValueError("There is no instance of the class with the specified name")
        
        if handler_type == "console":
            instance.__console_handler.setFormatter(logging.Formatter(format))
        elif handler_type == "file":
            instance.__file_handler.setFormatter(logging.Formatter(format))
        elif handler_type == "all":
            instance.__console_handler.setFormatter(logging.Formatter(format))
            instance.__file_handler.setFormatter(logging.Formatter(format))
        else:
            raise NotImplementedError(
                "The specified handler type is not valid\n" +
                "Valid handler types are: 'console', 'file', 'all'"
            )
            
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
        
        instance = MyLogger.__instances[logger_name]
        
        # Validate the log level
        if level.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"]:
            raise NotImplementedError(
                "The specified log level is not valid",
                "\n",
                "Valid log levels are: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET'",
            )
        
        # Configure the global log level
        if handler_type == "global":
            instance.__logger.setLevel(level.upper())
        elif handler_type == "console":
            instance.__console_handler.setLevel(level.upper())
        elif handler_type == "file":
            instance.__file_handler.setLevel(level.upper())
        elif handler_type == "all":
            instance.__console_handler.setLevel(level.upper())
            instance.__file_handler.setLevel(level.upper())

        else:
            raise NotImplementedError(
                "The specified handler type is not valid",
                "\n",
                "Valid handler types are: 'console', 'file', 'all', 'global'",
            )

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
    
