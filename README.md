# 🚀 Bitestream

> A production-inspired real-time food delivery analytics platform built using Apache Kafka, PySpark Structured Streaming, dbt, BigQuery, FastAPI, and Next.js.

![Project Status](https://img.shields.io/badge/status-In%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Apache Kafka](https://img.shields.io/badge/Apache-Kafka-black)
![PySpark](https://img.shields.io/badge/PySpark-Streaming-orange)
![BigQuery](https://img.shields.io/badge/Google-BigQuery-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

Bitestream is a real-time analytics platform that simulates a modern food delivery ecosystem similar to Swiggy, Zomato, or Uber Eats.

The platform continuously ingests delivery events, processes them using a streaming data pipeline, transforms them into business-ready datasets, and exposes operational insights through REST APIs and an interactive dashboard.

Rather than building a customer-facing food delivery application, Bitestream focuses on the internal analytics platform used by operations teams, restaurant partners, business analysts, and executives.

---

## 🎯 Problem Statement

Food delivery companies generate millions of events every day.

Each customer order creates multiple events such as:

- Order Created
- Restaurant Accepted
- Food Preparation Started
- Delivery Partner Assigned
- Picked Up
- Delivered
- Cancelled
- Customer Rating Submitted

Processing these events in real time enables businesses to monitor operational performance, detect bottlenecks, and make data-driven decisions.

Bitestream demonstrates how a modern streaming data platform can process these events with low latency and transform them into actionable business insights.

---

## 🏗️ High-Level Architecture

```
                Event Generator
                       │
                       ▼
                Apache Kafka
                       │
                       ▼
        PySpark Structured Streaming
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Bronze Layer                  Monitoring Logs
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
      dbt Models
        │
        ▼
      FastAPI
        │
        ▼
 Next.js Analytics Dashboard
```

---

## ✨ Key Features

- Real-time event ingestion
- Apache Kafka streaming pipeline
- PySpark Structured Streaming
- Bronze, Silver, and Gold data architecture
- Data transformations using dbt
- Google BigQuery as the analytical warehouse
- REST APIs using FastAPI
- Interactive dashboard with Next.js
- Dockerized local development environment
- End-to-end monitoring and logging

---

## 🛠️ Technology Stack

| Layer | Technologies |
|--------|--------------|
| Programming | Python |
| Streaming | Apache Kafka |
| Processing | PySpark Structured Streaming |
| Data Warehouse | Google BigQuery |
| Transformations | dbt |
| Backend | FastAPI |
| Frontend | Next.js, React, Tailwind CSS |
| Containerization | Docker |
| Version Control | Git, GitHub |

---

## 📂 Repository Structure

```
bitestream/

├── architecture/
├── backend/
├── data/
├── dbt/
├── docker/
├── docs/
├── frontend/
├── infrastructure/
├── monitoring/
├── scripts/
├── streaming/
├── tests/
├── README.md
└── docker-compose.yml
```

---

## 📊 Planned Dashboard

The analytics dashboard will provide:

- Live Orders
- Revenue Analytics
- Restaurant Performance
- Driver Performance
- Delivery SLA Monitoring
- Customer Ratings
- Order Funnel
- City-wise Analytics
- Peak Hour Analysis
- Cancellation Insights

---

## 📅 Development Roadmap

- [x] Repository Initialization
- [ ] Project Planning
- [ ] Event Generator
- [ ] Kafka Producer
- [ ] Kafka Consumer
- [ ] PySpark Structured Streaming
- [ ] Bronze Layer
- [ ] Silver Layer
- [ ] Gold Layer
- [ ] BigQuery Integration
- [ ] dbt Models
- [ ] FastAPI Backend
- [ ] Next.js Dashboard
- [ ] Docker Deployment
- [ ] CI/CD Pipeline
- [ ] Production Documentation

---

## 🎯 Learning Objectives

This project demonstrates practical implementation of:

- Event-Driven Architecture
- Streaming Data Processing
- Data Engineering Best Practices
- Medallion Architecture
- Data Modeling
- Incremental Processing
- REST API Development
- Dashboard Development
- Containerization
- Production Project Organization

---

## 📜 License

This project is licensed under the MIT License.