#!/bin/bash
# Entrypoint script for Docker Prober Utility

set -e

# Install Python dependencies (if not already installed)
pip install --no-cache-dir flask

# Start the Flask app
exec python3 app.py
