#!/usr/bin/env bash
set -e

# Default port 8080 for Cloud Run
PORT="${PORT:-8080}"

# Pass through the working directory that contains the ADK “apps”
# For you it’s the mytripmate folder (where you normally run `adk web`).
cd /app

# Launch ADK web bound to 0.0.0.0 so Cloud Run/LB can reach it.
# Most ADK builds forward these to uvicorn; if your ADK version
# ignores them, it will still run on 8000—Cloud Run will proxy to 8080.
exec adk web --host 0.0.0.0 --port "${PORT}"
