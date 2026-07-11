-- Gold-layer fact table for orders
CREATE TABLE IF NOT EXISTS `bitestream.gold.fct_orders` (
  order_id STRING NOT NULL,
  user_id STRING,
  restaurant_id STRING,
  order_time TIMESTAMP,
  delivered_time TIMESTAMP,
  total_amount NUMERIC,
  delivery_duration_seconds INT64
);
