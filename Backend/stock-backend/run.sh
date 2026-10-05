#!/bin/sh
set -eu

PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"

exec uv run uvicorn stock_backend.main:app --reload --host 127.0.0.1 --port 8000 "$@"
