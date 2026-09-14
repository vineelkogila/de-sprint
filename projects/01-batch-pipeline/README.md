# Project 1 — Batch Data Pipeline

## Objective

Build a batch ETL pipeline that reads order data from a CSV file, validates and transforms the records, and loads valid records into PostgreSQL.

## Architecture

CSV
↓
Python ETL
↓
Validation & Transformation
├── Valid records → PostgreSQL
└── Invalid records → Rejected
↓
Analytics Views
├── daily_sales
└── customer_sales

## Tech Stack

- Python
- PostgreSQL
- Docker
- psycopg
- python-dotenv
- Git

## Data Quality Rules

The pipeline rejects records when:

- `order_id` is not positive
- `quantity` is not positive
- `unit_price` is not positive

## Idempotency

The pipeline uses:

```sql
ON CONFLICT (order_id) DO NOTHING