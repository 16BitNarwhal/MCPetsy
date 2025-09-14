#!/usr/bin/env bash
# Render Chrome installation script
set -o errexit

# Save the current directory (where render.yaml and requirements.txt are)
ORIGINAL_DIR=$(pwd)
STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $ORIGINAL_DIR  # Return to where we started
else
  echo "...Using Chrome from cache"
fi

# Check Chrome version for debugging
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version

# Install uv (Python package manager that browser-use needs)
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install Python dependencies (requirements.txt is in starting directory)
pip install -r requirements.txt

# Install Playwright browsers (needed for browser-use)
echo "Installing Playwright browsers..."
python -m playwright install chromium

echo "Build complete"
