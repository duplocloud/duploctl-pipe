#!/usr/bin/env bash
set -e

echo "Setting up duploctl-pipe development environment..."

# Create necessary directories
mkdir -p config dist

# Optional: Create Python virtual environment
# Set DUPLO_USE_VENV=1 to enable venv creation in .venv directory
# This is automatically enabled in devcontainer environments
if [ "${DUPLO_USE_VENV}" = "1" ]; then
  echo "Creating Python virtual environment in .venv..."
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  echo "Virtual environment activated: $(which python)"
fi

# Install duploctl-pipe in editable mode with all dev dependencies
pip install --editable '.[build,test]'

echo "Setup complete!"
