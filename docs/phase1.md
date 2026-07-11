# Bitestream — Phase 1: Infrastructure Setup

## Overview

Phase 1 establishes the local streaming foundation for Bitestream: a
production-inspired Apache Kafka cluster (KRaft), Kafka UI, automated topic
bootstrap, centralized Kafka configuration, and a minimal producer/consumer
smoke test that proves end-to-end connectivity.

**Status:** Complete

---

## Goals

- Run Apache Kafka in KRaft mode (no ZooKeeper) via Docker Compose
- Expose Kafka UI for topic and message inspection
- Persist broker data across restarts
- Create the primary topic `food_delivery_events`
- Centralize Kafka connection settings in `configs/kafka_config.py`
- Validate Python → Kafka → Python message flow

## Non-Goals

- Event Generator / Faker-based synthetic traffic
- PySpark Structured Streaming
- FastAPI, dbt, BigQuery, or frontend
- Business logic, retries, or production auth/TLS

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│  Host (Windows + WSL2 / Docker Desktop)                     │
│                                                             │
│  producer/producer.py  ──localhost:9092──►  Kafka (KRaft)   │
│  consumer/consumer.py  ◄──localhost:9092──  food_delivery_  │
│                                              events         │
│                                                             │
│  Browser ──localhost:8080──► Kafka UI                       │
└─────────────────────────────────────────────────────────────┘
         │                              │
         │         bitestream-net       │
         ▼                              ▼
   bitestream-kafka              bitestream-kafka-ui
   (broker + controller)         (provectuslabs/kafka-ui)
         │
         ▼
   kafka-init-topics
   (one-shot topic bootstrap)
         │
         ▼
   volume: bitestream-kafka-data
```

### Dual listeners

| Listener | Address | Used by |
|----------|---------|---------|
| `PLAINTEXT` | `bitestream-kafka:29092` | Containers on `bitestream-net` |
| `PLAINTEXT_HOST` | `localhost:9092` | Host apps (producer / consumer) |
| `CONTROLLER` | `bitestream-kafka:29093` | KRaft metadata (internal only) |

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Docker Compose stack | `docker/docker-compose.yml` |
| Environment config | `docker/.env` / `docker/.env.example` |
| Topic init script | `docker/kafka/init-topics.sh` |
| Shared Kafka config | `configs/kafka_config.py` |
| Smoke producer | `producer/producer.py` |
| Smoke consumer | `consumer/consumer.py` |
| Smoke test runbook | `docs/phase1_smoke_test.md` |

---

## Services

| Service | Container | Ports | Restart |
|---------|-----------|-------|---------|
| Kafka (KRaft) | `bitestream-kafka` | `9092` → host | `${DOCKER_RESTART_POLICY}` |
| Topic init | `bitestream-kafka-init` | none | `no` (one-shot) |
| Kafka UI | `bitestream-kafka-ui` | `8080` → host | `${DOCKER_RESTART_POLICY}` |

**Images (pinned):**

- `confluentinc/cp-kafka:7.9.0`
- `provectuslabs/kafka-ui:v0.7.2`

---

## Topic

| Property | Value |
|----------|-------|
| Name | `food_delivery_events` |
| Partitions | 3 |
| Replication factor | 1 |
| Created by | `docker/kafka/init-topics.sh` |

---

## Shared Configuration

`configs/kafka_config.py` is the single source of truth for client apps:

| Constant | Value |
|----------|-------|
| `BOOTSTRAP_SERVERS` | `localhost:9092` |
| `TOPIC_NAME` | `food_delivery_events` |
| `CLIENT_ID` | `bitestream` |
| `CONSUMER_GROUP_ID` | `bitestream-smoke-test` |

Helpers:

- `get_producer_config()` → `bootstrap.servers`, `client.id`
- `get_consumer_config()` → `bootstrap.servers`, `group.id`, `auto.offset.reset`

---

## Quick Start

### 1. Start infrastructure

```powershell
cd d:\Project\bitestream\docker
Copy-Item .env.example .env   # first time only, if needed
docker compose up -d
docker compose ps
```

### 2. Open Kafka UI

[http://localhost:8080](http://localhost:8080)

### 3. Install smoke-test dependencies

```powershell
cd d:\Project\bitestream
python -m pip install -r producer\requirements.txt
python -m pip install -r consumer\requirements.txt
```

### 4. Run smoke test

```powershell
# Terminal 1
python consumer\consumer.py

# Terminal 2
python producer\producer.py
```

Detailed steps, expected output, checklist, and troubleshooting:
→ [`docs/phase1_smoke_test.md`](phase1_smoke_test.md)

---

## Validation Checklist

- [x] Kafka runs in KRaft mode (no ZooKeeper)
- [x] Kafka UI accessible at http://localhost:8080
- [x] Named volume persists broker data
- [x] Topic `food_delivery_events` exists (3 partitions, RF=1)
- [x] Init script is idempotent
- [x] Producer publishes exactly 10 events
- [x] Consumer receives exactly 10 events and exits
- [x] Configuration centralized in `configs/kafka_config.py`
- [x] No Event Generator / Faker / business logic in Phase 1

---

## Shutdown

```powershell
cd d:\Project\bitestream\docker

# Stop containers (keep data)
docker compose down

# Stop and wipe Kafka data volume
docker compose down -v
```

---

## What Comes Next

| Phase | Focus |
|-------|-------|
| **Phase 2** | Event Generator — continuous realistic food-delivery traffic |
| **Phase 3** | PySpark Structured Streaming — bronze / silver / gold |
| Later | FastAPI, dbt, BigQuery, monitoring, frontend |

Phase 2+ should import `BOOTSTRAP_SERVERS`, `TOPIC_NAME`, and the helper
config functions from `configs/kafka_config.py` rather than hardcoding
connection details.
