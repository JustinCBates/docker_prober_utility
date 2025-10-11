#!/bin/bash
# Pre-check script for Docker Prober Utility

# Check for Python 3.x
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.x is not installed."
    echo "Install Python 3.x using your package manager. Example: sudo apt-get install python3"
    exit 1
fi

# Check for python3-pip
if ! python3 -m pip --version &> /dev/null; then
    echo "Error: python3-pip is not installed."
    echo "Install pip using your package manager. Example: sudo apt-get install python3-pip"
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Install Docker using your package manager. Example: sudo apt-get install docker.io"
    exit 1
fi

echo "Python 3.x and Docker are installed."
