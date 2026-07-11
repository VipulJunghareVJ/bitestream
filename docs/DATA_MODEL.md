# 📄 Data Model

**Project:** Bitestream

**Version:** 1.0

**Status:** In Development

**Author:** Vipul Junghare

**Last Updated:** July 2026

---

# 1. Purpose

The Bitestream Data Model defines the core business entities and their relationships within the food delivery ecosystem.

It serves as the foundation for:

- Event Generation
- Kafka Event Schema
- Spark Processing
- Bronze, Silver and Gold Layers
- BigQuery Tables
- dbt Models
- REST APIs
- Analytics Dashboard

The data model represents the business domain and is independent of any specific database implementation.

---

# 2. Business Domain

Bitestream simulates a modern food delivery company.

The primary business workflow is:

Customer
↓

Places Order
↓

Restaurant Accepts Order
↓

Food Prepared
↓

Driver Assigned
↓

Order Picked Up
↓

Order Delivered
↓

Customer Rates Order

---

# 3. Core Business Entities

Bitestream consists of the following entities:

- Customer
- Restaurant
- Driver
- Order
- Delivery
- Payment
- Rating

---

# 4. Entity Relationship Diagram

```

                    Customer
                       │
                       │ Places
                       ▼
                    Order
                  /   |    \
                 /    |     \
                ▼     ▼      ▼
         Restaurant Payment Delivery
                               │
                               ▼
                            Driver
                               │
                               ▼
                             Rating

```

---

# 5. Entity Definitions

## 5.1 Customer

Represents the customer placing food orders.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| customer_id | String | Unique customer identifier |
| first_name | String | Customer first name |
| last_name | String | Customer last name |
| email | String | Customer email |
| phone | String | Contact number |
| city | String | Customer city |
| membership_type | String | Regular, Silver, Gold |
| created_at | Timestamp | Registration date |

---

## 5.2 Restaurant

Represents restaurant partners.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| restaurant_id | String | Unique restaurant identifier |
| restaurant_name | String | Restaurant name |
| cuisine | String | Cuisine type |
| city | String | Restaurant location |
| rating | Decimal | Average rating |
| opening_time | Time | Opening time |
| closing_time | Time | Closing time |

---

## 5.3 Driver

Represents delivery partners.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| driver_id | String | Unique driver identifier |
| driver_name | String | Driver name |
| vehicle_type | String | Bike, Scooter, Car |
| city | String | Operating city |
| status | String | Available, Busy, Offline |
| joining_date | Date | Joining date |

---

## 5.4 Order

Represents a customer's food order.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| order_id | String | Unique order identifier |
| customer_id | String | Customer placing the order |
| restaurant_id | String | Restaurant fulfilling the order |
| order_status | String | Current order status |
| subtotal | Decimal | Food amount |
| delivery_fee | Decimal | Delivery charge |
| tax_amount | Decimal | Tax amount |
| discount_amount | Decimal | Applied discount |
| total_amount | Decimal | Final payable amount |
| created_at | Timestamp | Order creation time |

---

## 5.5 Delivery

Represents the delivery process.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| delivery_id | String | Delivery identifier |
| order_id | String | Associated order |
| driver_id | String | Assigned driver |
| pickup_time | Timestamp | Pickup time |
| estimated_delivery_time | Timestamp | Estimated delivery |
| actual_delivery_time | Timestamp | Actual delivery |
| delivery_status | String | Current delivery status |

---

## 5.6 Payment

Represents payment information.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| payment_id | String | Payment identifier |
| order_id | String | Related order |
| payment_method | String | UPI, Card, Wallet, COD |
| payment_status | String | Success, Failed |
| amount | Decimal | Paid amount |
| payment_timestamp | Timestamp | Payment time |

---

## 5.7 Rating

Represents customer feedback.

### Attributes

| Attribute | Data Type | Description |
|------------|-----------|-------------|
| rating_id | String | Rating identifier |
| order_id | String | Related order |
| customer_id | String | Customer identifier |
| restaurant_rating | Integer | Restaurant rating (1–5) |
| driver_rating | Integer | Driver rating (1–5) |
| comments | String | Customer review |
| created_at | Timestamp | Rating submission time |

---

# 6. Entity Relationships

| Parent Entity | Child Entity | Relationship |
|---------------|--------------|--------------|
| Customer | Order | One-to-Many |
| Restaurant | Order | One-to-Many |
| Order | Payment | One-to-One |
| Order | Delivery | One-to-One |
| Driver | Delivery | One-to-Many |
| Order | Rating | One-to-One |

---

# 7. Business Rules

The following business rules govern the data model:

- A customer can place multiple orders.
- An order belongs to exactly one customer.
- An order is prepared by one restaurant.
- A restaurant can receive many orders.
- Each completed order has one payment.
- Each completed order has one delivery.
- A driver can deliver multiple orders over time.
- A customer may submit one rating per completed order.
- Cancelled orders do not have delivery records.
- Failed payments prevent order confirmation.

---

# 8. Entity Lifecycle

```

Customer

↓

Places Order

↓

Restaurant Accepts

↓

Payment Completed

↓

Driver Assigned

↓

Order Picked Up

↓

Order Delivered

↓

Customer Rating

```

---

# 9. Future Enhancements

Future versions of Bitestream may introduce additional entities such as:

- Menu Items
- Coupons
- Campaigns
- Refunds
- Customer Addresses
- Delivery Zones
- Restaurant Employees
- Live GPS Tracking
- Promotional Offers
- Loyalty Rewards

---

# 10. Next Steps

This data model will be transformed into:

- Kafka Event Schema
- Bronze Layer Tables
- Silver Layer Tables
- Gold Layer Tables
- BigQuery Warehouse
- dbt Models
- Dashboard KPIs

---

# End of Document