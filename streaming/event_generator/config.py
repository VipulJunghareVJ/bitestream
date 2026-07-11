"""Configuration for event generation and Kafka connectivity.

``GeneratorConfig`` is the Phase 2 synthetic-data settings object.
``KafkaConfig`` is a transitional client config used by early streaming
scaffolding. Prefer ``configs.kafka_config`` for new producer/consumer code.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env(key: str, default: str) -> str:
    """Read an environment variable with a fallback default."""
    return os.getenv(key, default)


@dataclass
class GeneratorConfig:
    """Synthetic data generation settings for the event generator."""

    cities: list[str] = field(
        default_factory=lambda: ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai"]
    )
    cuisines: list[str] = field(
        default_factory=lambda: ["Italian", "Indian", "Chinese", "Mexican", "Thai", "American"]
    )
    memberships: list[str] = field(default_factory=lambda: ["Normal", "Silver", "Gold"])
    vehicle_types: list[str] = field(default_factory=lambda: ["Bike", "Scooter", "Car"])
    payment_methods: list[str] = field(default_factory=lambda: ["UPI", "Card", "Wallet", "COD"])
    event_types: list[str] = field(
        default_factory=lambda: [
            "ORDER_CREATED",
            "ORDER_ACCEPTED",
            "FOOD_PREPARATION_STARTED",
            "FOOD_READY",
            "DRIVER_ASSIGNED",
            "ORDER_PICKED_UP",
            "ORDER_DELIVERED",
            "ORDER_CANCELLED",
            "PAYMENT_COMPLETED",
            "CUSTOMER_RATED",
        ]
    )
    schema_version: str = "1.0"
    source: str = "event_generator"
    producer_name: str = "bitestream"


@dataclass
class KafkaConfig:
    """Kafka broker and topic settings (transitional; see module docstring)."""

    bootstrap_servers: str = field(default_factory=lambda: _env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
    topic: str = field(default_factory=lambda: _env("KAFKA_TOPIC", "food_delivery_events"))
    client_id: str = field(default_factory=lambda: _env("KAFKA_CLIENT_ID", "bitestream"))
    consumer_group: str = field(default_factory=lambda: _env("KAFKA_CONSUMER_GROUP", "bitestream-consumer"))

    def producer_config(self) -> dict:
        """Return confluent-kafka Producer configuration."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "client.id": self.client_id,
        }

    def consumer_config(self) -> dict:
        """Return confluent-kafka Consumer configuration."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.consumer_group,
            "auto.offset.reset": "earliest",
        }


generator_config = GeneratorConfig()
kafka_config = KafkaConfig()
