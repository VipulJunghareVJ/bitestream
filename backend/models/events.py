"""Pydantic models for BiteStream events and API responses."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    event_time: datetime
    producer: str
    payload: dict


class ActiveOrders(BaseModel):
    active_orders: int


class AvgDeliveryTime(BaseModel):
    window: str
    avg_delivery_seconds: int
