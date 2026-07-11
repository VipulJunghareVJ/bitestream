"""Generate synthetic driver entities."""
from __future__ import annotations

import random
import uuid
from typing import Any

from streaming.event_generator.config import generator_config


def generate_driver_id() -> str:
    return f"DRV{uuid.uuid4().hex[:3].upper()}"


def generate_driver() -> dict[str, Any]:
    return {
        "driver_id": generate_driver_id(),
        "vehicle_type": random.choice(generator_config.vehicle_types),
    }
