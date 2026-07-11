# BiteStream — Architecture

## High-Level Flow

```
Producers -> Kafka -> Spark Structured Streaming -> Data Lake (bronze/silver/gold)
                                                         |
                                                         v
                                            Warehouse (BigQuery) + dbt
                                                         |
                                                         v
                                              Backend API -> Frontend
```

## Components

### Streaming (`streaming/`)
- **event_generator/** — synthetic food-delivery event traffic (Phase 2).
- **schemas/** — JSON schemas for Kafka events.

### Phase 1 smoke clients (repository root)
- **producer/** — infrastructure smoke-test producer (10 events).
- **consumer/** — infrastructure smoke-test consumer (exits after 10).
- Shared settings live in `configs/kafka_config.py`.

### Processing (`processing/`)
Medallion architecture with Spark:
- **bronze/** — raw ingested events.
- **silver/** — cleaned, deduplicated, conformed.
- **gold/** — business-level aggregates.
- **transformations/** — reusable transformation logic.

### Warehouse (`warehouse/`)
- **bigquery/** — loaders and dataset definitions.
- **sql/** — DDL and analytical queries.

### dbt (`dbt/`)
Models, tests, and documentation for warehouse transformations.

### Backend (`backend/`)
FastAPI service:
- **api/** — app entrypoint and wiring.
- **routers/** — HTTP route definitions.
- **services/** — business logic.
- **models/** — Pydantic/data models.

### Frontend (`frontend/`)
Dashboard application consuming the backend API.

### Monitoring (`monitoring/`)
Metrics, dashboards, and alerting configuration.

## Configuration
Centralized in `configs/` (Kafka, Spark, and general settings), driven by
environment variables (see `.env.example`).
