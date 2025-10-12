"""
Test fixtures and configuration for prober unit tests.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
import json


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def mock_flask_app():
    """Mock Flask application for testing."""
    app = MagicMock()
    app.test_client = MagicMock()
    app.config = {}
    return app


@pytest.fixture
def sample_probe_data():
    """Sample probe data for testing."""
    return {
        "host_info": {
            "hostname": "test-host",
            "os": "Linux",
            "python_version": "3.11.0"
        },
        "docker_info": {
            "version": "20.10.0",
            "containers": 5
        },
        "timestamp": "2025-10-12T06:00:00Z"
    }


@pytest.fixture
def probe_data_file(tmp_path, sample_probe_data):
    """Create a temporary probe data JSON file."""
    data_file = tmp_path / "probe_data.json"
    with open(data_file, 'w') as f:
        json.dump(sample_probe_data, f)
    return data_file