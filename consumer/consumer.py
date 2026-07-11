"""Kafka consumer smoke test for Bitestream Phase 1 infrastructure validation.

Subscribes to ``food_delivery_events``, consumes exactly 10 JSON messages,
prints them in a readable format, then exits. This validates Kafka → consumer
connectivity only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from confluent_kafka import Consumer, KafkaException, Message

# Allow ``python consumer/consumer.py`` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from configs.kafka_config import TOPIC_NAME, get_consumer_config

EVENT_COUNT = 10
POLL_TIMEOUT_SECONDS = 1.0


def format_timestamp(msg: Message) -> str:
    """Return a human-readable Kafka message timestamp, if present.

    Args:
        msg: Consumed Kafka message.

    Returns:
        Formatted timestamp string, or ``n/a`` when unavailable.
    """
    ts_type, ts_value = msg.timestamp()
    if ts_type == -1:
        return "n/a"
    label = "CREATE_TIME" if ts_type == 1 else "LOG_APPEND_TIME"
    return f"{ts_value} ({label})"


def print_event(index: int, msg: Message, event: dict[str, Any]) -> None:
    """Pretty-print a received event with partition metadata.

    Args:
        index: 1-based receive sequence number.
        msg: Consumed Kafka message (partition, offset, timestamp).
        event: Deserialized JSON payload.
    """
    print(f"Received Event {index}")
    print(f"  partition : {msg.partition()}")
    print(f"  offset    : {msg.offset()}")
    print(f"  timestamp : {format_timestamp(msg)}")
    print(f"  payload   : {json.dumps(event, indent=2)}")
    print()


def main() -> None:
    """Consume exactly 10 events, then close the consumer gracefully."""
    consumer = Consumer(get_consumer_config())
    consumer.subscribe([TOPIC_NAME])
    print(f"Connected to Kafka — subscribed to '{TOPIC_NAME}'")
    print(f"Waiting for {EVENT_COUNT} events...\n")

    received = 0

    try:
        while received < EVENT_COUNT:
            msg = consumer.poll(POLL_TIMEOUT_SECONDS)

            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            try:
                event = json.loads(msg.value().decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                print(f"[ERROR] Failed to deserialize message: {exc}")
                continue

            received += 1
            print_event(received, msg, event)

        print("Consumer completed successfully")
    except KafkaException as exc:
        print(f"[ERROR] Kafka error: {exc}")
        raise
    finally:
        consumer.close()
        print("Consumer closed.")


if __name__ == "__main__":
    main()
