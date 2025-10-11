#!/bin/bash
# Run all unit tests for Docker Prober Utility

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "==> Running Docker Prober Utility Unit Tests"
echo ""

# Change to project directory
cd "$PROJECT_DIR"

# Run Flask app tests
echo "==> Running Flask app tests..."
python3 -m pytest CI_Tests/test_app.py -v || python3 -m unittest CI_Tests/test_app.py
echo ""

# Run collection script tests
echo "==> Running host info collection tests..."
python3 -m pytest CI_Tests/test_collect_host_info.py -v || python3 -m unittest CI_Tests/test_collect_host_info.py
echo ""

# Run viewer tests
echo "==> Running probe data viewer tests..."
python3 -m pytest CI_Tests/test_view_probe_data.py -v || python3 -m unittest CI_Tests/test_view_probe_data.py
echo ""

echo "==> All tests completed!"
