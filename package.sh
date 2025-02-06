#!/bin/bash

# Ensure the script exits on any error
set -e

# Create a distribution directory
mkdir -p dist

# Copy necessary files to the distribution directory
cp -r src dist/
cp -r scripts dist/
cp requirements.txt dist/
cp README.md dist/
cp LICENSE.txt dist/

# Create a ZIP file
zip -r vscode-platform.zip dist/

# Clean up the distribution directory
rm -rf dist/

# Print completion message
echo "Packaging complete. The package is available as vscode-platform.zip"

# Make the package file executable
chmod +x vscode-platform.zip

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Print completion message for virtual environment setup
echo "Virtual environment setup complete and dependencies installed."
