"""
API Server Entry Point for AI Research Assistant Enterprise
"""
import os
import uvicorn
from server.fastapi_app import app

if __name__ == "__main__":
    uvicorn.run(
        "server.fastapi_app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True if os.getenv("ENVIRONMENT") != "production" else False
    )