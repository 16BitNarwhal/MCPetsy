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

# Install Python dependencies (requirements.txt is in starting directory)
pip install -r requirements.txt

echo "Build complete"
