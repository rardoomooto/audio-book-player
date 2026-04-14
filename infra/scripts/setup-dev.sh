#!/usr/bin/env bash
set -euo pipefail

# Development environment bootstrap script (Linux/macOS)
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

echo "[dev-setup] Initializing Python venv and Node deps..."

# Python environment
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment (venv) ..."
  python3 -m venv venv
fi
source venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
fi

# Node/Frontend dependencies (workspaces in frontend/)
if command -v npm >/dev/null 2>&1; then
  if [ -d "frontend" ]; then
    echo "Installing Node.js workspace dependencies..."
    (cd frontend && npm install --workspaces)
  fi
else
  echo "Warning: npm not found. Skipping frontend dependencies installation."
fi

echo "[dev-setup] Done. Activate venv with: source venv/bin/activate"
