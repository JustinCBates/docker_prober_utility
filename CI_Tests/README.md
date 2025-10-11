# Unit Tests for Docker Prober Utility

This directory contains unit tests for **host-side scripts** only. Container-based components (Flask app) are tested through deployment and integration testing.

## Test Files

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
python3 -m unittest CI_Tests.test_collect_host_info.TestCollectHostInfo.test_collect_host_info_network
```

## Test Coverage

The tests cover:
- ✅ Host information collection
- ✅ Data structure validation
- ✅ JSON file I/O operations
- ✅ Error handling and edge cases
- ✅ Rich TUI and plain text fallback
- ✅ Command execution utilities

## What's NOT Tested Here

- ❌ Flask app endpoints (tested in container)
- ❌ Docker deployment (tested through deploy script)
- ❌ Container-specific functionality

These are validated through integration testing and deployment verification.

## Requirements

Tests require:
- Python 3.x
- Standard library modules (unittest, json, etc.)

**NO** Flask or container dependencies needed!

Optional:
- pytest (for enhanced test running)
- coverage (for code coverage reports)

## Continuous Integration

These tests are designed to run in CI/CD pipelines without Docker:
```yaml
# Example GitHub Actions
- name: Run tests
  run: ./CI_Tests/run_tests.sh
```

## Adding New Tests

When adding new **host-side** features:
1. Create test cases in the appropriate test file
2. Follow the existing pattern (setUp, test methods, tearDown)
3. Use descriptive test method names
4. Add assertions for expected behavior
5. Test both success and failure cases

**Note**: Only add tests for scripts that run on the host. Container tests belong elsewhere.
