# Phase 1 — Producer & Consumer Smoke Test

## 1. Objective

Validate end-to-end Kafka connectivity for the Bitestream Phase 1
infrastructure:

```text
Python Producer
        │
        ▼
food_delivery_events
        │
        ▼
Python Consumer
```

This is an infrastructure smoke test only. It does **not** implement the
Event Generator, Faker, or business logic.

---

## 2. Project Components

| Component | Path | Role |
|-----------|------|------|
| Kafka config | `configs/kafka_config.py` | Shared bootstrap, topic, client, and group settings |
| Producer | `producer/producer.py` | Publishes exactly 10 deterministic JSON events |
| Consumer | `consumer/consumer.py` | Consumes exactly 10 events and exits |
| Kafka broker | `docker/docker-compose.yml` | KRaft single-broker cluster |
| Kafka UI | http://localhost:8080 | Visual verification of topics and offsets |

---

## 3. Prerequisites

- Docker Desktop running (WSL2 backend recommended on Windows)
- Python 3.11+
- Phase 1 infrastructure already started (`kafka`, `kafka-ui`, topics initialized)
- Topic `food_delivery_events` exists (created by `docker/kafka/init-topics.sh`)

---

## 4. Installation

From the repository root:

```powershell
cd d:\Project\bitestream

python -m pip install -r producer\requirements.txt
python -m pip install -r consumer\requirements.txt
```

Both files pin:

```text
confluent-kafka==2.15.0
```

---

## 5. How to Start Kafka

```powershell
cd d:\Project\bitestream\docker
docker compose up -d
docker compose ps
```

Confirm:

- `bitestream-kafka` is **healthy**
- `bitestream-kafka-ui` is **healthy**
- Topic `food_delivery_events` exists (Kafka UI → Topics, or init container logs)

Kafka UI: [http://localhost:8080](http://localhost:8080)

---

## 6. How to Run the Consumer

**Start the consumer first** (Terminal 1), from the repository root:

```powershell
cd d:\Project\bitestream
python consumer\consumer.py
```

The consumer waits until it has received exactly 10 messages, then exits.

---

## 7. How to Run the Producer

**Then start the producer** (Terminal 2), from the repository root:

```powershell
cd d:\Project\bitestream
python producer\producer.py
```

The producer publishes exactly 10 events, flushes, and exits.

---

## 8. Expected Output

### Producer

```text
Connected to Kafka
Sent Event 1
Sent Event 2
...
Sent Event 10
[ACK] topic=food_delivery_events partition=... offset=...
Producer completed successfully
```

(`[ACK]` lines may appear interleaved as delivery callbacks fire.)

### Consumer

```text
Connected to Kafka — subscribed to 'food_delivery_events'
Waiting for 10 events...

Received Event 1
  partition : ...
  offset    : ...
  timestamp : ...
  payload   : {
    "order_id": "ORD-1001",
    "customer_id": "CUS-201",
    "restaurant_id": "RES-11",
    "status": "PLACED",
    "event_timestamp": "..."
  }

...

Received Event 10
...
Consumer completed successfully
Consumer closed.
```

---

## 9. Validation Checklist

- [ ] Producer connects successfully
- [ ] Consumer connects successfully
- [ ] Producer publishes exactly 10 events
- [ ] Consumer receives exactly 10 events
- [ ] JSON serialization / deserialization works
- [ ] No Kafka broker errors
- [ ] Kafka UI shows increasing offsets on `food_delivery_events`
- [ ] Configuration is centralized in `configs/kafka_config.py`
- [ ] No hardcoded bootstrap servers in producer/consumer business paths

---

## 10. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `Connection refused` / broker unavailable | Kafka not running | `cd docker; docker compose up -d` |
| Consumer hangs forever | Producer not started, or wrong topic | Start producer in Terminal 2; confirm topic name |
| Consumer exits with fewer than 10 messages | Interrupted early | Re-run consumer, then producer |
| Consumer receives old / unexpected messages | Shared consumer group already committed offsets | Start consumer **before** producer so it waits for new messages; or create a temporary group for debugging |
| `ModuleNotFoundError: configs` | Wrong working directory | Run from repository root: `d:\Project\bitestream` |
| `ModuleNotFoundError: confluent_kafka` | Dependency not installed | `pip install -r producer\requirements.txt` |
| Topic does not exist | Init job not run | Check `kafka-init-topics` logs; open Kafka UI → Topics |
| Port 9092 already in use | Another Kafka / process bound | Stop conflicting process or adjust host port in `docker/.env` (infra only) |

### Useful Commands

```powershell
# Broker health
cd d:\Project\bitestream\docker
docker compose ps

# List topics
docker compose exec kafka kafka-topics --bootstrap-server bitestream-kafka:29092 --list

# Describe smoke-test topic
docker compose exec kafka kafka-topics --bootstrap-server bitestream-kafka:29092 --describe --topic food_delivery_events
```
