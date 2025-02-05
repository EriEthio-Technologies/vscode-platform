#!/bin/bash

# Clear npm cache
npm cache clean --force

# Remove package-lock.json
rm -f package-lock.json

# Remove node_modules directory
rm -rf node_modules

echo "Cleaned npm cache, removed package-lock.json and node_modules"
