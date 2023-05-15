from .logger import MyLogger

class OliviaFinderException(Exception):
    """Base class for exceptions in this module."""
    
    def __init__(self, message, errors = None):    

        super().__init__(message)
        self.message = message
        self.errors = errors

        # Log the exception
        MyLogger().get_logger().warning(message)

    def __str__(self):
        '''String representation of the exception'''
        return f"EXCEPTION -> type: {self.__class__.__name__}, message: {self.message}, errors: {self.errors}"

