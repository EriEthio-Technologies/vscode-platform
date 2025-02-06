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

echo "Packaging complete. The package is available as vscode-platform.zip"
