#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Load .env if present
if [[ -f .env ]]; then
  export $(grep -v '^#' .env | xargs -d '\n' -I {} echo {}) || true
fi

exec python -m bot.main
