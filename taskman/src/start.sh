#!/bin/sh
set -e
python -u build.py
exec uvicorn server:app --host 0.0.0.0 --port ${API_AUTH_PORT}