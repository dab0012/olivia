'''
File:              load_config.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 7:25:53 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import configparser
import logging
import os
import sys

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

# Add the folder where the Firefox's selenium driver 
sys.path.append(config['selenium']['driver_path'])
