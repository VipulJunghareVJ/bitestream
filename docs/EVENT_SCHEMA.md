# 📄 Event Schema Design

**Project:** Bitestream

**Version:** 1.0

**Status:** In Development

**Author:** Vipul Junghare

**Last Updated:** July 2026

---

# 1. Purpose

Bitestream follows an **event-driven architecture** where every business action within the food delivery ecosystem is represented as an event.

These events are published to Apache Kafka, processed using PySpark Structured Streaming, transformed into analytical datasets, and eventually consumed by APIs and dashboards.

The Event Schema acts as the **single source of truth** for all events flowing through the platform.

---

# 2. Design Principles

The event schema follows these principles:

- Single canonical event structure
- Immutable events
- Schema versioning support
- Event timestamp driven
- Business-oriented entities
- Extensible for future enhancements
- Compatible with JSON serialization

---

# 3. Event Lifecycle

A typical food delivery order generates multiple events during its lifecycle.

```

Customer Places Order

↓

ORDER_CREATED

↓

ORDER_ACCEPTED

↓

FOOD_PREPARATION_STARTED

↓

FOOD_READY

↓

DRIVER_ASSIGNED

↓

ORDER_PICKED_UP

↓

ORDER_DELIVERED

↓

CUSTOMER_RATED

```

Each event represents a state transition in the order lifecycle.

---

# 4. Supported Event Types

| Event Type | Description |
|------------|-------------|
| ORDER_CREATED | Customer places an order |
| ORDER_ACCEPTED | Restaurant accepts the order |
| FOOD_PREPARATION_STARTED | Kitchen begins preparing food |
| FOOD_READY | Order is ready for pickup |
| DRIVER_ASSIGNED | Delivery partner assigned |
| ORDER_PICKED_UP | Driver picks up the order |
| ORDER_DELIVERED | Order successfully delivered |
| ORDER_CANCELLED | Order cancelled |
| PAYMENT_COMPLETED | Payment successful |
| CUSTOMER_RATED | Customer submits rating |

---

# 5. Canonical Event Structure

Every Kafka message follows the same structure.

```json
{
  "event_id": "evt_000001",
  "event_type": "ORDER_CREATED",
  "event_timestamp": "2026-07-06T18:30:15Z",

  "order": {},
  "customer": {},
  "restaurant": {},
  "driver": {},
  "payment": {},

  "metadata": {}
}
```

---

# 6. Entity Definitions

## 6.1 Order

```json
{
  "order_id": "ORD100001",
  "status": "CREATED",
  "total_amount": 480.50,
  "delivery_fee": 40,
  "tax_amount": 25,
  "discount_amount": 30
}
```

### Fields

| Field | Type | Description |
|------|------|-------------|
| order_id | String | Unique order identifier |
| status | String | Current order status |
| total_amount | Decimal | Total order amount |
| delivery_fee | Decimal | Delivery charge |
| tax_amount | Decimal | Tax collected |
| discount_amount | Decimal | Discount applied |

---

## 6.2 Customer

```json
{
  "customer_id": "CUS001",
  "city": "Bengaluru",
  "membership": "Gold"
}
```

| Field | Type | Description |
|------|------|-------------|
| customer_id | String | Customer identifier |
| city | String | Customer city |
| membership | String | Normal / Silver / Gold |

---

## 6.3 Restaurant

```json
{
  "restaurant_id": "RES100",
  "restaurant_name": "Pizza Palace",
  "cuisine": "Italian"
}
```

| Field | Type | Description |
|------|------|-------------|
| restaurant_id | String | Restaurant identifier |
| restaurant_name | String | Restaurant name |
| cuisine | String | Cuisine category |

---

## 6.4 Driver

```json
{
  "driver_id": "DRV120",
  "vehicle_type": "Bike"
}
```

| Field | Type | Description |
|------|------|-------------|
| driver_id | String | Driver identifier |
| vehicle_type | String | Bike / Scooter / Car |

---

## 6.5 Payment

```json
{
  "payment_method": "UPI",
  "payment_status": "SUCCESS"
}
```

| Field | Type | Description |
|------|------|-------------|
| payment_method | String | UPI / Card / Wallet / COD |
| payment_status | String | SUCCESS / FAILED |

---

## 6.6 Metadata

```json
{
  "source": "event_generator",
  "schema_version": "1.0",
  "producer": "bitestream"
}
```

| Field | Type | Description |
|------|------|-------------|
| source | String | Event source |
| schema_version | String | Schema version |
| producer | String | Producer application |

---

# 7. Complete Sample Event

```json
{
  "event_id": "evt_000001",
  "event_type": "ORDER_CREATED",
  "event_timestamp": "2026-07-06T18:30:15Z",

  "order": {
    "order_id": "ORD100001",
    "status": "CREATED",
    "total_amount": 480.50,
    "delivery_fee": 40,
    "tax_amount": 25,
    "discount_amount": 30
  },

  "customer": {
    "customer_id": "CUS001",
    "city": "Bengaluru",
    "membership": "Gold"
  },

  "restaurant": {
    "restaurant_id": "RES101",
    "restaurant_name": "Pizza Palace",
    "cuisine": "Italian"
  },

  "driver": {
    "driver_id": "DRV007",
    "vehicle_type": "Bike"
  },

  "payment": {
    "payment_method": "UPI",
    "payment_status": "SUCCESS"
  },

  "metadata": {
    "source": "event_generator",
    "schema_version": "1.0",
    "producer": "bitestream"
  }
}
```

---

# 8. Schema Versioning

Future schema changes should follow semantic versioning.

| Version | Description |
|----------|-------------|
| 1.0 | Initial event schema |
| 1.1 | Add optional fields |
| 2.0 | Breaking schema changes |

---

# 9. Event Processing Flow

```
Food Delivery Simulator
        │
        ▼
Generate JSON Event
        │
        ▼
Apache Kafka
        │
        ▼
PySpark Structured Streaming
        │
        ▼
Bronze Layer
        │
        ▼
Silver Layer
        │
        ▼
Gold Layer
        │
        ▼
BigQuery
        │
        ▼
Dashboard
```

---

# 10. Future Enhancements

Future versions may include:

- GPS coordinates
- Driver location updates
- Estimated delivery time (ETA)
- Weather conditions
- Traffic congestion
- Customer device information
- Restaurant preparation time
- Promotional campaign details
- Coupon information
- Fraud detection metadata

---

# End of Document