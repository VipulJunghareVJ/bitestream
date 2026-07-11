"""Kafka producer smoke test for Bitestream Phase 1 infrastructure validation.

Publishes exactly 10 deterministic JSON events to ``food_delivery_events``
and exits. This is not the event generator — it only proves producer → Kafka
connectivity.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from confluent_kafka import KafkaError, Message, Producer

# Allow ``python producer/producer.py`` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from configs.kafka_config import TOPIC_NAME, get_producer_config

EVENT_COUNT = 10


def delivery_report(err: KafkaError | None, msg: Message) -> None:
    """Handle asynchronous delivery acknowledgements from the broker.

    Args:
        err: Delivery error from librdkafka, or ``None`` on success.
        msg: The produced message metadata returned by the broker.
    """
    if err is not None:
        print(f"[ERROR] Delivery failed: {err}")
        return

    print(
        f"[ACK] topic={msg.topic()} partition={msg.partition()} "
        f"offset={msg.offset()}"
    )


def build_event(index: int) -> dict[str, Any]:
    """Build a deterministic sample food-delivery event.

    Args:
        index: 1-based event sequence number.

    Returns:
        A JSON-serializable event dictionary.
    """
    return {
        "order_id": f"ORD-{1000 + index}",
        "customer_id": f"CUS-{200 + index}",
        "restaurant_id": f"RES-{10 + index}",
        "status": "PLACED",
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    """Produce exactly 10 events, flush the producer, then exit."""
    producer = Producer(get_producer_config())
    print("Connected to Kafka")

    for i in range(1, EVENT_COUNT + 1):
        event = build_event(i)
        payload = json.dumps(event).encode("utf-8")

        try:
            producer.produce(
                TOPIC_NAME,
                key=event["order_id"].encode("utf-8"),
                value=payload,
                callback=delivery_report,
            )
            producer.poll(0)
            print(f"Sent Event {i}")
        except BufferError as exc:
            print(f"[ERROR] Local producer queue is full: {exc}")
            producer.poll(1)
            raise

    producer.flush()
    print("Producer completed successfully")


if __name__ == "__main__":
    main()
