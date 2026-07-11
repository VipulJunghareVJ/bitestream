"""FastAPI application entrypoint for BiteStream."""
from __future__ import annotations

from fastapi import FastAPI

from backend.routers import health, metrics

app = FastAPI(title="BiteStream API", version="0.1.0")

app.include_router(health.router)
app.include_router(metrics.router, prefix="/api/v1")
