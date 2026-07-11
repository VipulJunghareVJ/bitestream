# BiteStream — API Specification

Base URL: `/api/v1`

## Health
### `GET /health`
Returns service status.
```json
{ "status": "ok" }
```

## Metrics

### `GET /metrics/orders/active`
Current number of in-progress orders.
```json
{ "active_orders": 128 }
```

### `GET /metrics/delivery/avg-time`
Average delivery time over a window.

Query params: `window` (e.g. `15m`, `1h`, `24h`).
```json
{ "window": "1h", "avg_delivery_seconds": 1740 }
```

### `GET /metrics/revenue/daily`
Daily revenue, optionally filtered by city.

Query params: `date`, `city` (optional).
```json
{ "date": "2026-07-08", "city": "NYC", "revenue": 15230.75 }
```

## Errors
All errors follow:
```json
{ "detail": "message describing the error" }
```
Common codes: `400` (bad request), `404` (not found), `500` (server error).
