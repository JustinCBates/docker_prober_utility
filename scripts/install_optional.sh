#!/bin/bash
# Optional dependency installer for Docker Prober Utility
# Prompts user before installing optional packages like rich

set -e

echo "==> Docker Prober Utility - Optional Dependencies"
echo ""

# Check if rich is already installed
if python3 -c "import rich" 2>/dev/null; then
    echo "✓ Rich library is already installed"
    echo ""
    exit 0
fi

echo "The Rich library provides beautiful, colorful terminal output for viewing probe data."
echo ""
echo "Without Rich:"
echo "  - Probe data will be displayed as plain JSON"
echo "  - All functionality still works"
echo ""
echo "With Rich:"
echo "  - Beautiful formatted tables and panels"
echo "  - Color-coded output"
echo "  - Enhanced readability"
echo ""

read -p "Would you like to install Rich? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing Rich library..."
    if python3 -m pip install --user rich; then
        echo "✓ Rich installed successfully!"
        echo ""
        echo "You can now use:"
        echo "  python3 scripts/view_probe_data.py"
        echo ""
    else
        echo "✗ Failed to install Rich"
        echo "You can still view data as JSON:"
        echo "  cat probe_data.json"
        exit 1
    fi
else
    echo "Skipping Rich installation."
    echo "You can install it later by running this script again or:"
    echo "  pip install rich"
    echo ""
fi
