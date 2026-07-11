# BiteStream — Product Requirements

## Overview
BiteStream is a real-time food-delivery analytics platform. It ingests order,
delivery, and user events as they happen, processes them through a medallion
(bronze/silver/gold) architecture, and serves insights via an API and dashboard.

## Goals
- Capture live events (orders, deliveries, driver location, user activity).
- Provide near real-time metrics (active orders, avg delivery time, revenue).
- Enable historical analytics through a data warehouse.

## Non-Goals
- Payment processing.
- Restaurant menu management.

## Personas
- **Operations manager** — monitors live delivery health.
- **Data analyst** — explores historical trends.
- **Engineer** — maintains pipelines and services.

## Functional Requirements
1. Stream ingestion of events via Kafka.
2. Layered processing (bronze -> silver -> gold) with Spark.
3. Warehouse loading (BigQuery) and dbt transformations.
4. REST API exposing aggregated metrics.
5. Frontend dashboard visualizing key KPIs.

## Success Metrics
- End-to-end event latency < 30s.
- 99.5% pipeline uptime.
