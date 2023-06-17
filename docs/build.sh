#!/bin/bash

# pip install pdoc

# Añadiar al path el directorio de olivia_finder
export PYTHONPATH=$PYTHONPATH:$(pwd)/olivia_finder/

# Añadir al path el fichero de configuración de olivia_finder
export OLIVIA_FINDER_CONFIG_FILE_PATH=$(pwd)/olivia_finder/config.ini


# Si se ha usado el flag --theme dark, se añade el css de dark mode
# Se sobrescribe el fichero de tema original de pdoc en el venv .venv/lib/python3.9/site-packages/pdoc/templates/theme.css
if [ "$1" == "--theme" ] && [ "$2" == "dark" ]; then
    cp docs/css/dark_theme.css .venv/lib/python3.10/site-packages/pdoc/templates/theme.css
else
    cp docs/css/default_theme.css .venv/lib/python3.10/site-packages/pdoc/templates/theme.css
fi

# Remove old docs
rm -rf docs/olivia_finder docs/*.html docs/*.js 

if [ "$1" == "--server" ]; then
    # Run server
    pdoc olivia_finder/lib/olivia_finder \
    --footer-text "Olivia Finder Doc, by Daniel Alonso Báscones" \
    --logo https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/logo.png \
    --favicon https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/favicon.ico \
    --logo-link https://github.com/dab0012/olivia-finder/
    exit 0

else
    # Generate new docs
    pdoc \
        -d numpy \
        -o docs olivia_finder/lib/olivia_finder \
        --footer-text "Olivia Finder Doc, by Daniel Alonso Báscones" \
        --logo https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/logo.png \
        --favicon https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/favicon.ico \
        --logo-link https://github.com/dab0012/olivia-finder/
    
    exit 0
fi
