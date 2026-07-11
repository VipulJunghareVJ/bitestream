"""Centralized Kafka configuration for Bitestream.

Shared by the Phase 1 smoke-test producer/consumer, the upcoming event
generator (Phase 2), and future PySpark Structured Streaming jobs (Phase 3).

This module holds connection settings and helper functions only.
It does not contain producer/consumer business logic.
"""

from __future__ import annotations

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "food_delivery_events"
CLIENT_ID = "bitestream"
CONSUMER_GROUP_ID = "bitestream-smoke-test"


def get_producer_config() -> dict[str, str]:
    """Build confluent-kafka Producer configuration.

    Returns:
        A dict with ``bootstrap.servers`` and ``client.id``.
    """
    return {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "client.id": CLIENT_ID,
    }


def get_consumer_config() -> dict[str, str]:
    """Build confluent-kafka Consumer configuration.

    Returns:
        A dict with ``bootstrap.servers``, ``group.id``, and
        ``auto.offset.reset`` set to ``earliest``.
    """
    return {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": CONSUMER_GROUP_ID,
        "auto.offset.reset": "earliest",
    }
