# Blockhouse Capital – Software Engineer Intern

## Work Trial Assignment
**Overview:**  
A production-ready microservice that fetches market data, processes it through a streaming pipeline (Kafka), stores raw and processed data in PostgreSQL, and serves it via REST APIs with FastAPI. Demonstrates clean code, documentation, and DevOps best practices.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Running the Service](#running-the-service)
- [API Endpoints](#api-endpoints)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Message Schema](#message-schema)
- [Repository Structure](#repository-structure)
- [Troubleshooting](#troubleshooting)
- [Video Walkthrough](#video-walkthrough)

---

## Prerequisites

- Docker & Docker Compose  
- Git  
- Optional: Python 3.10+ for local venv

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/himanshu8655/blockhouse-assessment.git
   cd blockhouse-assessment
   ```
2. **Environment variables:**  
   Create a `.env` file in project root (Already provided in Git for easy setup):
   ```env
   DATABASE_URL=postgresql://root:root@postgres:5432/blockhouse
   REDIS_URL=redis://redis:6379
   KAFKA_BOOTSTRAP_SERVERS=kafka:9092
   PROVIDER=yfinance
   ```
3. **Start services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   This will pull images, build the FastAPI service, and launch PostgreSQL, Redis, Zookeeper, Kafka, and your API.

---

## Running the Service

The API will be available at `http://localhost:8000`.  
Open interactive docs: `http://localhost:8000/docs`.

---

## API Endpoints

### GET `/prices/latest`
Fetch the latest price for a symbol.

**Query Parameters:**
- `symbol` (string, required)
- `provider` (string, optional)

**Response:**
```json
{
    "symbol": "AAPL",
    "price": 196.4499969482422,
    "timestamp": "2025-06-13T15:59:00+00:00",
    "provider": "yahoo"
}
```

### POST `/prices/poll`
Start polling job for symbols.

**Body:**
```json
{
  "symbols": ["AAPL", "MSFT"],
  "interval": 60,
  "provider": "yahoo_finance"
}

```

**Response (202 Accepted):**
```json
{
    "job_id": "poll_7e585bc2",
    "status": "accepted",
    "config": {
        "symbols": [
            "AAPL",
            "MSFT"
        ],
        "interval": 60
    }
}
```

---

## Architecture

### System Architecture Diagram

\`\`\`mermaid
graph TB
    subgraph "Market Data Service"
        API["FastAPI Service"]
        DB[(PostgreSQL)]
        Cache["Redis Cache"]
    end
    subgraph "Message Queue"
        K["Kafka"]
        ZK["ZooKeeper"]
        Producer["Price Producer"]
        Consumer["MA Consumer"]
    end
    subgraph "External Services"
        MarketAPI["Market Data API"]
    end

    Client["Client App"] --> API
    API --> DB
    API --> Cache
    API --> MarketAPI
    API --> Producer
    Producer --> K
    K --> Consumer
    Consumer --> DB
    ZK <--> K
\`\`\`

### Flow Diagram

\`\`\`mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI
    participant M as Market API
    participant K as Kafka
    participant MA as MA Consumer
    participant DB as PostgreSQL

    C->>A: GET /prices/latest
    A->>Cache: Check cache
    alt Cache miss
        A->>M: Fetch price
        M-->>A: Price data
        A->>DB: Store raw
        A->>K: Produce event
    end
    A-->>C: Return response

    K->>MA: Consume event
    MA->>DB: Fetch last 5
    MA->>MA: Compute MA
    MA->>DB: Store MA
\`\`\`

---

## Database Schema

- **raw_responses**: stores raw market API JSON  
- **price_points**: individual price entries  
- **symbol_averages**: 5-point moving averages  
- **poll_jobs**: polling job configs

Indexes on `(symbol, timestamp)` for performance.

---

## Message Schema

\`\`\`json
{
  "symbol": "AAPL",
  "price": 150.25,
  "timestamp": "2024-03-20T10:30:00Z",
  "source": "alpha_vantage",
  "raw_response_id": "uuid-here"
}
\`\`\`

---

## Repository Structure

\`\`\`
market-data-service/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── schemas/
├── tests/
├── docs/
├── .github/workflows/
├── requirements/
├── docker-compose.yml
└── Dockerfile
\`\`\`

---

## Postman CURL
- API POST /prices/poll

curl --location 'http://localhost:8000/prices/poll' \
--header 'Content-Type: application/json' \
--data '{
  "symbols": ["AAPL", "MSFT"],
  "interval": 60,
  "provider": "yfinance"
}
'

- API GET /prices/latest
curl --location 'http://localhost:8000/prices/latest?symbol=AAPL'
---


## Troubleshooting

- **DB connection errors:** Ensure containers are up (`docker-compose ps`).  
- **Kafka startup issues:** Remove old ZK nodes (`docker-compose down -v`).  
- **Missing env vars:** Verify `.env` file in root.

---

## Video Walkthrough

A 5‑minute walkthrough video is available in link `https://youtu.be/6bCCHDhando`.

