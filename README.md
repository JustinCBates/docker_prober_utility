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

- Python 3.x
- Flask
- Docker (for containerization)

To install Python dependencies:
```bash
pip install flask
```

To build and run the Docker container, Docker must be installed on the host.
## License
MIT
