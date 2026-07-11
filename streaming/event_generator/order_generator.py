"""Generate synthetic order entities."""
from __future__ import annotations

import random
import uuid
from typing import Any


def generate_order_id() -> str:
    return f"ORD{uuid.uuid4().hex[:6].upper()}"


def generate_order(status: str = "CREATED") -> dict[str, Any]:
    subtotal = round(random.uniform(150.0, 1200.0), 2)
    delivery_fee = round(random.uniform(20.0, 60.0), 2)
    tax_amount = round(subtotal * 0.05, 2)
    discount_amount = round(random.uniform(0.0, 80.0), 2)
    total_amount = round(subtotal + delivery_fee + tax_amount - discount_amount, 2)

    return {
        "order_id": generate_order_id(),
        "status": status,
        "total_amount": total_amount,
        "delivery_fee": delivery_fee,
        "tax_amount": tax_amount,
        "discount_amount": discount_amount,
    }
