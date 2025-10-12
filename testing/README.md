# Testing Framework - Prober

This directory contains the comprehensive testing framework for the prober component.

## 🎯 **Testing Philosophy**

We use a structured approach to testing with clear separation of concerns:
- **Unit Tests**: Test individual probing components in isolation
- **Integration Tests**: Test data collection workflows and Flask endpoints  
- **End-to-End Tests**: Test complete probing scenarios and TUI workflows

## 📁 **Directory Structure**

```
testing/
├── unit/                    # Unit tests (fast, isolated)
│   ├── conftest.py         # Unit test fixtures
│   └── __init__.py
├── integration/            # Integration tests (components working together)
│   ├── test_collect_host_info.py    # Host information collection tests (moved from CI_Tests)
│   ├── test_view_probe_data.py      # Data visualization tests (moved from CI_Tests)
│   ├── conftest.py         # Integration test fixtures  
│   └── __init__.py
├── e2e/                    # End-to-end tests (full workflows)
│   ├── conftest.py         # E2E test fixtures
│   └── __init__.py
├── scripts/                # Test execution scripts
│   ├── run_unit_tests.py   # Run only unit tests
│   ├── run_integration_tests.py  # Run only integration tests  
│   ├── run_e2e_tests.py    # Run only e2e tests
│   └── run_all_tests.py    # Run complete test suite
├── config/                 # Test configuration
│   └── pytest.ini         # Pytest configuration
├── results/                # Test results and reports
├── documentation/          # Testing guides and documentation
│   ├── testing_guide.md    # Comprehensive testing guide
│   └── framework_overview.md  # Testing framework overview
└── README.md              # This file
```

## 🚀 **Quick Start**

### Run All Tests
```bash
cd testing
python scripts/run_all_tests.py
```

### Run Specific Test Types
```bash
# Unit tests only (fast)
python scripts/run_unit_tests.py

# Integration tests only (includes original CI tests)
python scripts/run_integration_tests.py

# End-to-end tests only
python scripts/run_e2e_tests.py
```

### Run Tests with Pytest Directly
```bash
# From project root
pytest testing/unit/ -v                    # Unit tests
pytest testing/integration/ -v             # Integration tests (includes original CI_Tests)
pytest testing/e2e/ -v                     # E2E tests
pytest testing/ -v                         # All tests
```

## 📊 **Current Test Coverage**

- **Unit Tests**: Flask app components, data collection functions
- **Integration Tests**: ✅ Host info collection, probe data visualization (migrated from CI_Tests)
- **E2E Tests**: TBD - Complete probing workflows, TUI interactions

## 🔧 **Adding New Tests**

### Unit Tests
- Add to `testing/unit/`
- Focus on testing individual probing functions/classes
- Use mocks for system calls and Flask components
- Should run in <1 second each

### Integration Tests  
- Add to `testing/integration/`
- Test probing component interactions
- May use actual system resources and file I/O
- Acceptable to run in <30 seconds each

### End-to-End Tests
- Add to `testing/e2e/`
- Test complete probing workflows
- May take several minutes to run
- Test real data collection and visualization scenarios

## 📋 **Test Standards**

1. **Naming**: Test files must start with `test_`
2. **Documentation**: Each test should have a clear docstring
3. **Isolation**: Tests should not depend on each other
4. **Cleanup**: Tests should clean up files and resources they create
5. **Assertions**: Use descriptive assertion messages

## 🔄 **Migration from CI_Tests**

The original `CI_Tests/` directory has been integrated into this framework:
- `CI_Tests/test_collect_host_info.py` → `integration/test_collect_host_info.py`
- `CI_Tests/test_view_probe_data.py` → `integration/test_view_probe_data.py`
- `CI_Tests/run_tests.sh` → `scripts/run_integration_tests.py` (enhanced)

## 🔗 **Related Documentation**

- [`documentation/testing_guide.md`](documentation/testing_guide.md) - Comprehensive testing guide
- [`documentation/framework_overview.md`](documentation/framework_overview.md) - Framework architecture
- [`config/pytest.ini`](config/pytest.ini) - Pytest configuration details

This testing framework ensures reliability and maintainability of the prober component.