"""
FastAPI server entry point.

    python api_server.py                   # development
    uvicorn api_server:app --reload        # hot-reload dev
    uvicorn api_server:app --workers 4     # production
"""

import os
import uvicorn
from api.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8001)),
        log_level="info",
    )
