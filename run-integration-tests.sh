#!/bin/bash

PYTHONPATH=./ ./venv/bin/pytest test_integration $*
