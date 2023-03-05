'''
File:              config.py
Project:           Olivia-Finder
Created Date:      Friday March 3rd 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday March 3rd 2023 7:02:38 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import logging

class LoggerConfiguration:
    '''
    Class to configure the logger
    '''

    LOGGING_FORMAT = '%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filename, level):

        self.filename = filename
        self.level = level
        self.format = self.LOGGING_FORMAT
        self.date_format = self.LOGGING_DATE_FORMAT

    def aply_config(self) -> None:
        '''
        Apply the configuration to the logger
        '''
        logging.basicConfig(
            filename=self.filename,
            level=logging.getLevelName(self.level),
            format=self.format,
            datefmt=self.date_format
        )

        self.logger = logging.getLogger(__name__)

    def get_logger(self) -> logging.Logger:
        '''
        Get the logger
        '''
        return self.logger
    
