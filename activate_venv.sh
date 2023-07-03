#!/bin/bash

# Virtual environment name
venv_name=".venv"

# Check if the virtual environment exists
if [ -d "$venv_name" ]; then
    echo "Activating virtual env $venv_name ..."
    source "$venv_name/bin/activate"
    which python3
else
    echo "Creating virtual env $venv_name ..."
    python3 -m venv "$venv_name"
    source "$venv_name/bin/activate"
    pip install --upgrade pip
    which python3
    echo "Installing requirements..."
    # pip install -r olivia/requirements.txt
    pip install -r olivia_finder/requirements.txt
fi


