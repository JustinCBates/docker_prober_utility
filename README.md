## Usage Instructions

### Manual Usage
1. Run the pre-check script to verify Python and Docker installation:
	```bash
	bash scripts/precheck.sh
	```
2. Install dependencies if not already installed:
	```bash
	pip install flask rich
	```
3. Collect host information:
	```bash
	python3 scripts/collect_host_info.py
	```
4. View probe data with beautiful TUI:
	```bash
	python3 scripts/view_probe_data.py
	```
5. Or start the Flask app:
	```bash
	python3 app.py
	```

### Docker Usage
1. Use the deployment script (recommended):
	```bash
	./scripts/deploy.sh
	```
   This will build, run, collect data, and save to probe_data.json

2. Or manually build and run:
	```bash
	docker build -t prober .
	docker run -p 8080:8080 prober
	```

### Viewing Collected Data
- **Rich TUI Interface** (recommended):
  ```bash
  python3 scripts/view_probe_data.py
  ```
- **Raw JSON**:
  ```bash
  cat probe_data.json
  ```
- **Web Interface**:
  ```bash
  curl http://localhost:8080/probe
  ```

### Troubleshooting
- If you see errors about missing Python or Docker, run the `precheck.sh` script and follow the installation instructions provided.
- Ensure all dependencies are installed before starting the app manually.
# Docker Prober Utility

This utility provides a minimal HTTP/HTTPS backend for integration testing and deployment validation. It is designed to be included as a submodule in other projects (e.g., openproject-docker-compose) to test proxy and server configuration before full stack deployment.

## Features
- Minimal Hello World backend (Python Flask)
- Dockerfile for easy containerization
- Intended for use in CI/CD and manual integration tests

## Usage
Clone or include as a submodule:

```bash
git submodule add https://github.com/JustinCBates/docker_prober_utility.git proxy/integration_test/prober
```

Build and run:

```bash
cd proxy/integration_test/prober
docker build -t prober .
docker run -p 8080:8080 prober
```

## Control Flow
1. Build the Docker image
2. Run the container
3. Probe HTTP/HTTPS endpoints
4. Tear down after validation

## Critical Host Information for Docker Stack Configuration
When configuring a Docker stack, extract the following information from the host:

- **Host Network Configuration**: Network interfaces, IP addresses, open ports, firewall rules
- **Resource Availability**: CPU, memory, disk space, swap
- **Operating System Details**: OS type/version, kernel version, installed packages
- **Docker Environment**: Docker version, Compose version, daemon status
- **Environment Variables**: Required variables, secrets, credentials
- **Volume and Mount Points**: Storage paths, permissions
- **Proxy and DNS Settings**: Proxy configuration, DNS settings
- **Time Zone and Locale**: Host time zone, locale

This information ensures the Docker stack is configured correctly and services operate reliably.

## Dependencies
This project requires the following dependencies:

**Required:**
- Python 3.x
- Flask
- Docker (for containerization)
- python3-pip (for installing Python packages)
- python3-venv (for creating virtual environments)

**Optional:**
- Rich (for beautiful terminal output)

To install required Python dependencies:
```bash
pip install flask
```

To install optional Rich library for enhanced TUI:
```bash
./scripts/install_optional.sh
# or manually:
pip install rich
```

To build and run the Docker container, Docker must be installed on the host.
## License
MIT
