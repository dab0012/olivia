#!/bin/bash

# Virtual environment name
venv_name=".venv"

# Check if the virtual environment exists
if [ -d "$venv_name" ]; then
    echo "Activating virtual atmosphere $venv_name ..."
    source "$venv_name/bin/activate"
    which python3
else
    echo "Creating virtual atmosphere $venv_name ..."
    python3 -m venv "$venv_name"
    source "$venv_name/bin/activate"
    which python3
    echo "Installing requirements..."
    pip install -r requirements.txt
fi
