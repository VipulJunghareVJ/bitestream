"""Build canonical food-delivery events for the Bitestream pipeline."""
from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone
from typing import Any

from streaming.event_generator.config import generator_config
from streaming.event_generator.driver_generator import generate_driver
from streaming.event_generator.order_generator import generate_order
from streaming.event_generator.restaurant_generator import generate_restaurant

ORDER_STATUS_BY_EVENT = {
    "ORDER_CREATED": "CREATED",
    "ORDER_ACCEPTED": "ACCEPTED",
    "FOOD_PREPARATION_STARTED": "PREPARING",
    "FOOD_READY": "READY",
    "DRIVER_ASSIGNED": "DRIVER_ASSIGNED",
    "ORDER_PICKED_UP": "PICKED_UP",
    "ORDER_DELIVERED": "DELIVERED",
    "ORDER_CANCELLED": "CANCELLED",
    "PAYMENT_COMPLETED": "PAID",
    "CUSTOMER_RATED": "RATED",
}


def generate_customer() -> dict[str, Any]:
    return {
        "customer_id": f"CUS{uuid.uuid4().hex[:3].upper()}",
        "city": random.choice(generator_config.cities),
        "membership": random.choice(generator_config.memberships),
    }


def generate_payment(event_type: str) -> dict[str, Any]:
    if event_type == "ORDER_CANCELLED":
        status = "FAILED"
    elif event_type in {"ORDER_DELIVERED", "PAYMENT_COMPLETED", "CUSTOMER_RATED"}:
        status = "SUCCESS"
    else:
        status = random.choice(["SUCCESS", "SUCCESS", "PENDING"])

    return {
        "payment_method": random.choice(generator_config.payment_methods),
        "payment_status": status,
    }


def generate_event(event_type: str | None = None) -> dict[str, Any]:
    """Return a single event matching the canonical food-delivery schema."""
    event_type = event_type or random.choice(generator_config.event_types)
    order_status = ORDER_STATUS_BY_EVENT.get(event_type, "CREATED")

    return {
        "event_id": f"evt_{uuid.uuid4().hex[:8]}",
        "event_type": event_type,
        "event_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "order": generate_order(status=order_status),
        "customer": generate_customer(),
        "restaurant": generate_restaurant(),
        "driver": generate_driver(),
        "payment": generate_payment(event_type),
        "metadata": {
            "source": generator_config.source,
            "schema_version": generator_config.schema_version,
            "producer": generator_config.producer_name,
        },
    }


def generate_event_stream(count: int, interval_seconds: float = 1.0):
    """Yield a sequence of events for simulation."""
    import time

    for _ in range(count):
        yield generate_event()
        time.sleep(interval_seconds)
