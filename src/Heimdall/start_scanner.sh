#!/bin/bash

python3 -m venv env
source env/bin/activate
pip install -r heimdall/requirements.txt
python3 -m heimdall.main
