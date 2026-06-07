#!/bin/bash

echo "Creating Virtual Environment..."

python -m venv .venv

source .venv/bin/activate

echo "Installing Dependencies..."

pip install -r backend/requirements.txt

echo "Setup Completed Successfully!"
