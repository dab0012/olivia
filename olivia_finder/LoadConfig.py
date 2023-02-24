# Author: Daniel Alonso Báscones
# Email:  dab0012 at alu.ubu.es
# Project: Olivia Finder
# Description: This module implements the configuration loading

import configparser
import logging

# Load the configuration from the file
config = configparser.ConfigParser()
config.read('config.ini')

# Configure logging from the [logging] section
logging.basicConfig(
    filename=config['logging']['filename'],
    level=logging.getLevelName(config['logging']['level']),
    format=config['logging']['format']
)

