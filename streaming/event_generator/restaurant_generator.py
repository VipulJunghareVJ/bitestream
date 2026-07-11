"""Generate synthetic restaurant entities."""
from __future__ import annotations

import random
import uuid
from typing import Any

from streaming.event_generator.config import generator_config

RESTAURANT_NAMES = [
    "Pizza Palace",
    "Spice Garden",
    "Burger Barn",
    "Sushi Express",
    "Curry House",
    "Taco Town",
    "Noodle Nook",
    "Grill Master",
]


def generate_restaurant_id() -> str:
    return f"RES{uuid.uuid4().hex[:3].upper()}"


def generate_restaurant() -> dict[str, Any]:
    return {
        "restaurant_id": generate_restaurant_id(),
        "restaurant_name": random.choice(RESTAURANT_NAMES),
        "cuisine": random.choice(generator_config.cuisines),
    }
