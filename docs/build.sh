#!/bin/bash


pip install pdoc

# Remove old docs
rm -rf docs/olivia_finder docs/*.html docs/*.js 

# Generate new docs
pdoc -o docs olivia_finder/lib/olivia_finder --footer-text "Olivia Finder Doc, by Daniel Alonso Báscones"  --logo https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/logo.png --favicon https://raw.githubusercontent.com/dab0012/olivia-finder/master/docs/img/favicon.ico --logo-link https://github.com/dab0012/olivia-finder/
