# Bitestream

> A production-inspired real-time food delivery analytics platform built using Apache Kafka, PySpark Structured Streaming, dbt, BigQuery, FastAPI, and Next.js.

![Project Status](https://img.shields.io/badge/status-Phase%201%20Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Apache Kafka](https://img.shields.io/badge/Apache-Kafka-KRaft-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

Bitestream is a real-time analytics platform that simulates a modern food delivery ecosystem similar to Swiggy, Zomato, or Uber Eats.

The platform continuously ingests delivery events, processes them using a streaming data pipeline, transforms them into business-ready datasets, and exposes operational insights through REST APIs and an interactive dashboard.

Rather than building a customer-facing food delivery application, Bitestream focuses on the internal analytics platform used by operations teams, restaurant partners, business analysts, and executives.

---

## Current Status — Phase 1 Complete

Phase 1 delivers the local streaming foundation:

- Apache Kafka in **KRaft mode** (no ZooKeeper)
- Kafka UI for topic and message inspection
- Automated topic bootstrap for `food_delivery_events`
- Centralized Kafka config in `configs/kafka_config.py`
- Python producer / consumer smoke test

Full Phase 1 details: [`docs/phase1.md`](docs/phase1.md)

---

## High-Level Architecture

```text
                Event Generator (Phase 2)
                       │
                       ▼
                Apache Kafka (Phase 1 ✓)
                       │
                       ▼
        PySpark Structured Streaming (Phase 3)
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Bronze Layer                  Monitoring Logs
        │
        ▼
 Silver Layer → Gold Layer → BigQuery → dbt
                                         │
                                         ▼
                              FastAPI → Next.js Dashboard
```

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| Windows 10/11 + WSL2 | Or Linux / macOS |
| Docker Desktop | Compose v2+ |
| Python 3.11+ | For smoke-test producer / consumer |
| Git | Version control |

---

## Phase 1 — Setup & Usage

### 1. Clone the repository

```powershell
git clone <repository-url>
cd bitestream
```

### 2. Configure Docker environment

```powershell
cd docker
Copy-Item .env.example .env
```

Edit `docker/.env` only if you need to change ports or hostnames.

### 3. Start Kafka infrastructure

```powershell
cd docker
docker compose up -d
docker compose ps
```

Expected healthy services:

| Service | Container | Access |
|---------|-----------|--------|
| Kafka (KRaft) | `bitestream-kafka` | `localhost:9092` |
| Kafka UI | `bitestream-kafka-ui` | [http://localhost:8080](http://localhost:8080) |
| Topic init | `bitestream-kafka-init` | one-shot (exits after creating topics) |

Topic created automatically: **`food_delivery_events`** (3 partitions, RF=1)

### 4. Install smoke-test dependencies

From the repository root:

```powershell
cd d:\Project\bitestream
python -m pip install -r producer\requirements.txt
python -m pip install -r consumer\requirements.txt
```

### 5. Run the producer / consumer smoke test

**Terminal 1 — start the consumer first:**

```powershell
cd d:\Project\bitestream
python consumer\consumer.py
```

**Terminal 2 — then run the producer:**

```powershell
cd d:\Project\bitestream
python producer\producer.py
```

Expected result:

- Producer prints `Sent Event 1` … `Sent Event 10` and `Producer completed successfully`
- Consumer prints `Received Event 1` … `Received Event 10` and `Consumer completed successfully`

### 6. Verify in Kafka UI

1. Open [http://localhost:8080](http://localhost:8080)
2. Select cluster **bitestream-cluster**
3. Open **Topics** → `food_delivery_events` → **Messages**
4. Confirm JSON payloads and increasing offsets

### 7. Stop infrastructure

```powershell
cd d:\Project\bitestream\docker

# Stop containers (keep Kafka data)
docker compose down

# Stop and wipe Kafka data volume
docker compose down -v
```

---

## Project Structure (Phase 1)

```text
bitestream/
├── configs/
│   └── kafka_config.py          # Shared Kafka settings
├── producer/
│   ├── producer.py              # Smoke-test producer (10 events)
│   └── requirements.txt
├── consumer/
│   ├── consumer.py              # Smoke-test consumer (exits after 10)
│   └── requirements.txt
├── docker/
│   ├── docker-compose.yml       # Kafka + Kafka UI + topic init
│   ├── .env.example
│   └── kafka/
│       └── init-topics.sh       # Idempotent topic bootstrap
├── docs/
│   ├── phase1.md                # Phase 1 overview
│   ├── phase1_smoke_test.md     # Smoke-test runbook
│   └── ...
├── streaming/
│   ├── event_generator/         # Synthetic traffic (Phase 2)
│   └── schemas/                 # Event JSON schemas
├── processing/                  # PySpark medallion (Phase 3+)
├── backend/                     # FastAPI stubs (later)
├── frontend/                    # Dashboard (later)
├── warehouse/                   # BigQuery SQL stubs (later)
├── dbt/                         # dbt project stub (later)
└── README.md
```

---

## Technology Stack

| Layer | Technologies |
|--------|--------------|
| Programming | Python 3.11 |
| Streaming | Apache Kafka (KRaft), confluent-kafka |
| Processing | PySpark Structured Streaming *(planned)* |
| Data Warehouse | Google BigQuery *(planned)* |
| Transformations | dbt *(planned)* |
| Backend | FastAPI *(planned)* |
| Frontend | Next.js *(planned)* |
| Containerization | Docker Compose |
| Version Control | Git, GitHub |

---

## Development Roadmap

- [x] Repository initialization
- [x] **Phase 1 — Infrastructure** (Kafka KRaft, Kafka UI, topic init)
- [x] **Phase 1 — Smoke test** (producer / consumer + shared config)
- [ ] Phase 2 — Event Generator
- [ ] Phase 3 — PySpark Structured Streaming (bronze / silver / gold)
- [ ] BigQuery integration
- [ ] dbt models
- [ ] FastAPI backend
- [ ] Next.js dashboard
- [ ] Monitoring & CI/CD

---

## Documentation

| Doc | Description |
|-----|-------------|
| [`docs/phase1.md`](docs/phase1.md) | Phase 1 architecture, services, checklist |
| [`docs/phase1_smoke_test.md`](docs/phase1_smoke_test.md) | Smoke-test install, run, troubleshooting |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Platform architecture |
| [`docs/PRODUCT_REQUIREMENTS.md`](docs/PRODUCT_REQUIREMENTS.md) | Product requirements |
| [`docs/EVENT_SCHEMA.md`](docs/EVENT_SCHEMA.md) | Event schemas |
| [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) | Data model |

---

## Troubleshooting (Quick)

| Issue | Fix |
|-------|-----|
| Port 9092 / 8080 in use | Change `KAFKA_HOST_PORT` / `KAFKA_UI_HOST_PORT` in `docker/.env` |
| `Connection refused` | Run `docker compose up -d` from `docker/` |
| `ModuleNotFoundError: configs` | Run scripts from the repository root |
| Consumer hangs | Start consumer first, then producer |
| Topic missing | Check `kafka-init-topics` logs; open Kafka UI → Topics |

More detail: [`docs/phase1_smoke_test.md`](docs/phase1_smoke_test.md)

---

## License

This project is licensed under the MIT License.
