# Author: Daniel Alonso Báscones
# Email:  dab0012 at alu.ubu.es
# Project: Olivia Finder
# Description: This module implements the configuration loading

import configparser
import logging
import os

# Load the configuration from the file
config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

# Configure logging from the [logging] section
logging.basicConfig(
    filename=config['logging']['filename'],
    level=logging.getLevelName(config['logging']['level']),
    format=config['logging']['format']
)

