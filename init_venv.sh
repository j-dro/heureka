#!/bin/bash

if ! [ -d ./venv ]; then
    python3 -m venv ./venv
fi

./venv/bin/pip3 install --upgrade pip
./venv/bin/pip3 install -r ./requirements.txt
