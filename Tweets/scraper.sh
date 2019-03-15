#!/bin/bash

export CONSUMER_KEY=$1
export CONSUMER_SECRET=$2
export ACCESS_TOKEN=$3
export ACCESS_SECRET=$4

source venv/bin/activate
python3 __main__.py
deactivate
