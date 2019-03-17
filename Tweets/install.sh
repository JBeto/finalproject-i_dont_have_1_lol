#!/bin/bash

python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m virtualenv venv -p python3.6
source venv/bin/activate
python3 -m pip install -r requirements.txt
deactivate
