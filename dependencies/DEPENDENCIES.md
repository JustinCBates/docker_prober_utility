# Dependencies for Prober

## Production Dependencies (Required for all users)

### Absolute (Always needed)
- python>=3.8                  # Python runtime
- flask                        # Web framework (from app.py)

### Ad Hoc (Needed for optional features)
- requests                     # HTTP requests (if probing external services)
- psutil                       # System information (if monitoring system resources)
- docker                       # Docker integration (if probing containers)

## Developer Dependencies (Only needed for development)

### Absolute (Core development tools)
- python>=3.8                  # Python runtime
- pytest                       # Testing framework

### Ad Hoc (Optional development tools)
- black                        # Code formatting (if formatting Python code)
- flake8                       # Code linting (if linting Python code)
- coverage                     # Test coverage (if measuring coverage)

## Installation Commands

### Production Only (Minimal)
```bash
pip3 install flask
```

### With Optional Features
```bash
# HTTP probing
pip3 install requests

# System monitoring
pip3 install psutil

# Docker integration
pip3 install docker
```

### Development Environment
```bash
pip3 install pytest black flake8 coverage
```

## Notes
- Flask app requires Python and Flask
- Additional dependencies added as features are developed
- Tests in CI_Tests/ directory use pytest
- Update this file when adding new dependencies or features