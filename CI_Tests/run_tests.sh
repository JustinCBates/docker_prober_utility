#!/bin/bash
# Run unit tests for Docker Prober Utility (host-side scripts only)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "==> Running Docker Prober Utility Unit Tests (Host Scripts)"
echo ""

# Change to project directory
cd "$PROJECT_DIR"

# Run collection script tests
echo "==> Running host info collection tests..."
python3 -m pytest CI_Tests/test_collect_host_info.py -v 2>/dev/null || python3 -m unittest CI_Tests/test_collect_host_info.py
echo ""

# Run viewer tests
echo "==> Running probe data viewer tests..."
python3 -m pytest CI_Tests/test_view_probe_data.py -v 2>/dev/null || python3 -m unittest CI_Tests/test_view_probe_data.py
echo ""

echo "==> All host-side tests completed!"
echo ""
echo "Note: Flask app tests are not included here as they require"
echo "the container environment. The app is tested through deployment."
