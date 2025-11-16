#!/bin/bash
# Jelastic deployment hook - runs after code update

echo "Installing Python dependencies..."
pip install -r /var/www/webroot/ROOT/requirements.txt --break-system-packages --user

echo "Dependencies installed successfully"
