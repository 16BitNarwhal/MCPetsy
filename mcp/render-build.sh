#!/usr/bin/env bash
# Render Chrome installation script
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/mcp # Return to project root where requirements.txt is
else
  echo "...Using Chrome from cache"
fi

# Check Chrome version for debugging
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version

# Install Python dependencies (from project root)
cd $HOME/mcp
pip install -r requirements.txt

echo "Build complete"
