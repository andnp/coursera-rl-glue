#!/bin/bash
set -e

export PYTHONPATH=RlGlue
python3 -m unittest discover -p "*test_*.py"
