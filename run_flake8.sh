#!/bin/bash

SRC_DIR=./

python3 -m flake8 --ignore=D203 ${SRC_DIR}/autonomous_agent.py
