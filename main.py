"""
main.py — Railway entry point.

Railway auto-detects this file. It re-exports the FastAPI `app` object
from api_server.py so uvicorn can be pointed at `main:app`.
"""

from api.app import create_app

app = create_app()
