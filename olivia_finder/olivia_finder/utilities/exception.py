from .logger import MyLogger


class OliviaFinderException(Exception):
    """Base class for exceptions in this module."""
    
    def __init__(self, message: str):
        
        self.message = message
        super().__init__(self.message)

        # Log the exception
        MyLogger().get_logger().debug(self.message)