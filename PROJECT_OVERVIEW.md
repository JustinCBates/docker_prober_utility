# Project Overview: Docker Prober Utility

## Purpose
A minimal HTTP/HTTPS backend (Python Flask) for integration testing and deployment validation. Designed to be included in other projects to test proxy and server configuration before full stack deployment.

## Key Features
- Minimal Flask backend (app.py)
- Dockerfile for containerization
- Entrypoint script (entrypoint.sh) for starting the app
- Utility scripts in `scripts/` (e.g., precheck.sh)
- Persists probe results in `probe_data.json` (untracked)
- Unit tests in `test_app.py`

## Directory Structure
- `app.py`: Flask backend
- `entrypoint.sh`: Main entrypoint script
- `Dockerfile`: Container build instructions
- `probe_data.json`: Stores probe results (excluded from git)
- `scripts/`: Utility scripts (e.g., precheck.sh)
- `test_app.py`: Unit tests
- `.gitignore`: Excludes probe_data.json and other files

## Usage
- Manual: Run `entrypoint.sh` after verifying dependencies
- Docker: Build and run container using Dockerfile
- Pre-check: Use `scripts/precheck.sh` to verify Python and Docker

## Dependencies
- Python 3.x
- Flask
- Docker


## How to Restore Context
Read this file for a summary of project goals, structure, and usage. Review the README.md for more details.
