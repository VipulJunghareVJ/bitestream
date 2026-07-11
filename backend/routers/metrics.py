"""Metrics routes exposing aggregated analytics."""
from __future__ import annotations

from fastapi import APIRouter, Query

from backend.services import metrics_service

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/orders/active")
def active_orders() -> dict:
    return {"active_orders": metrics_service.get_active_orders()}


@router.get("/delivery/avg-time")
def avg_delivery_time(window: str = Query("1h")) -> dict:
    return {
        "window": window,
        "avg_delivery_seconds": metrics_service.get_avg_delivery_seconds(window),
    }
