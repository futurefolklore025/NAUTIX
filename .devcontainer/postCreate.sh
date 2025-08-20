#!/usr/bin/env bash
set -euo pipefail

# Backend venv
cd /workspaces/$(basename "$PWD")/backend || cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt || true

echo "Devcontainer setup complete"
