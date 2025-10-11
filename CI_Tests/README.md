# Unit Tests for Docker Prober Utility

This directory contains comprehensive unit tests for all components of the Docker Prober Utility.

## Test Files

- **test_app.py**: Tests for Flask application endpoints
  - Root endpoint (`/`)
  - Health check (`/health`)
  - Probe data endpoint (`/probe`)
  - Collection trigger (`/collect`)
  - Test/validation endpoint (`/test`)

- **test_collect_host_info.py**: Tests for host information collection
  - Command execution utilities
  - Data collection functions
  - JSON file operations
  - Data structure validation

- **test_view_probe_data.py**: Tests for probe data viewer
  - Data loading and validation
  - Plain text display
  - Rich TUI display (when available)
  - Table creation functions

## Running Tests

### Run all tests:
```bash
./CI_Tests/run_tests.sh
```

### Run individual test files:
```bash
# Flask app tests
python3 -m unittest CI_Tests/test_app.py

# Collection script tests
python3 -m unittest CI_Tests/test_collect_host_info.py

# Viewer tests
python3 -m unittest CI_Tests/test_view_probe_data.py
```

### Run with pytest (if installed):
```bash
pytest CI_Tests/ -v
```

### Run specific test:
```bash
python3 -m unittest CI_Tests.test_app.ProberTestCase.test_health_endpoint
```

## Test Coverage

The tests cover:
- ✅ All Flask API endpoints
- ✅ Data collection functionality
- ✅ JSON file I/O operations
- ✅ Error handling and edge cases
- ✅ Rich TUI and plain text fallback
- ✅ Data structure validation

## Requirements

Tests require:
- Python 3.x
- Flask (for app tests)
- Standard library modules (unittest, json, etc.)

Optional:
- pytest (for enhanced test running)
- coverage (for code coverage reports)

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run tests
  run: ./CI_Tests/run_tests.sh
```

## Adding New Tests

When adding new features:
1. Create test cases in the appropriate test file
2. Follow the existing pattern (setUp, test methods, tearDown)
3. Use descriptive test method names
4. Add assertions for expected behavior
5. Test both success and failure cases
