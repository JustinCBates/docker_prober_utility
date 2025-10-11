
#!/bin/bash
# Entrypoint script for Docker Prober Utility

set -e

# Check for python3
if ! command -v python3 &> /dev/null; then
	echo "Error: python3 is not installed. Please install Python 3.x."
	exit 1
fi

VENV_DIR=".venv"

# Create a local virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
	echo "Creating virtual environment in $VENV_DIR..."
	if python3 -m venv "$VENV_DIR" 2>/dev/null; then
		echo "Virtual environment created."
		source "$VENV_DIR/bin/activate"
		python -m pip install --upgrade pip
		python -m pip install --no-cache-dir flask
		exec "$VENV_DIR/bin/python" app.py
	else
		echo "Could not create virtual environment. Trying user-site pip install as fallback..."
		if python3 -m pip --version &> /dev/null; then
			echo "Installing dependencies to user site-packages..."
			python3 -m pip install --user --no-cache-dir flask || true
			echo "You can run the app with: python3 app.py (and ensure PYTHONPATH includes user site-packages)"
			exec python3 app.py
		else
			echo "Neither virtualenv nor pip (for user-install) is available."
			echo "On Debian/Ubuntu: sudo apt install python3-venv python3-pip"
			echo "Or create a virtual environment on another machine and run the app there."
			exit 1
		fi
	fi
else
	# venv exists; activate and run
	source "$VENV_DIR/bin/activate"
	python -m pip install --upgrade pip
	python -m pip install --no-cache-dir flask
	exec "$VENV_DIR/bin/python" app.py
fi


