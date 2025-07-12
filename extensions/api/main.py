"""
FastAPI interface for Enhanced Trading Agents
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

# Load configuration
config_path = Path("configs/default.json")
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
else:
    config = {"api": {"cors_origins": ["*"]}}

app = FastAPI(
    title="Enhanced Trading Agents API",
    description="Multi-threaded stock analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["api"].get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Enhanced Trading Agents API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers
# from .routers import analysis, stocks, results
# app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
# app.include_router(stocks.router, prefix="/api/v1", tags=["stocks"]) 
# app.include_router(results.router, prefix="/api/v1", tags=["results"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
