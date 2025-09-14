#!/usr/bin/env bash
# Render Chrome installation script
set -o errexit

# Save the current directory (where render.yaml and requirements.txt are)
ORIGINAL_DIR=$(pwd)
STORAGE_DIR=/opt/render/project/.render

# Skip system dependencies - Render's environment is read-only
echo "Skipping system dependencies due to read-only filesystem..."

# Skip manual Chrome installation - use only Playwright's Chromium
echo "Using Playwright's Chromium instead of manual Chrome installation"

# Install uv (Python package manager that browser-use needs)
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install Python dependencies (requirements.txt is in starting directory)
pip install -r requirements.txt

# Install Playwright browsers (without --with-deps due to read-only filesystem)
echo "Installing Playwright browsers..."
python -m playwright install chromium

echo "Build complete"
