# Backend — FastAPI + PostgreSQL + Redis + Celery

## Overview
This backend provides APIs for product management, CSV ingestion, webhook handling, and asynchronous task execution. It is built using FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis, and Celery. CSV files are uploaded through an endpoint and processed in the background using Celery workers.

---

# Requirements
- Python 3.10+
- Docker
- Node.js (optional, for frontend)
- PostgreSQL (via Docker)
- Redis (via Docker)

---

# Project Structure
```
app/
  main.py
  db.py
  models.py
  schemas.py
  deps.py
  config.py
  celery_app.py
  tasks.py
  routers/
    upload.py
    products.py
    progress.py
migrations/
.env
```

---

# Environment Setup

## 1. Create & activate virtual environment

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

Verify environment:
```bash
which python
python --version
```

---

## 2. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg[binary] python-multipart celery redis python-dotenv
```

---

## 3. Create `.env` file
Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+psycopg://yogesh:Pass@123@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
UPLOAD_DIR=/tmp/acme_uploads
```

---

# Database Setup (PostgreSQL via Docker)

## 1. Run PostgreSQL container
```bash
docker run -d \
  --name my-postgres-db \
  -e POSTGRES_PASSWORD=Pass@123 \
  -e POSTGRES_USER=yogesh \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:latest
```

Verify:
```bash
docker ps
```

## 2. Connect to PostgreSQL
```bash
docker exec -it my-postgres-db psql -U yogesh -d mydb
```

---

# Database Migrations (Alembic)

## 1. Initialize Alembic
```bash
alembic init migrations
```

## 2. Configure `migrations/env.py`
Replace metadata section with:
```python
from app.db import Base
target_metadata = Base.metadata
```

## 3. Generate migration
```bash
alembic revision --autogenerate -m "init"
```

## 4. Apply migration
```bash
alembic upgrade head
```

---

# Redis Setup (for Celery)
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7
```

---

# Running the Backend

## 1. Start FastAPI server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API Docs:

- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc

---

## 2. Start Celery Worker (background processing)
Open another terminal and activate the venv:

```bash
celery -A app.celery_app.celery worker --loglevel=info --concurrency=2
```

---

# API Overview

## CSV Upload
```
POST /upload/
multipart/form-data: file=@yourfile.csv
```

Track progress:
```
GET /progress/{job_id}
```

Real-time stream:
```
GET /progress/stream/{job_id}
```

---

## Product Management
| Method | Endpoint               | Description          |
|--------|-------------------------|----------------------|
| GET    | `/products`             | List products        |
| POST   | `/products`             | Create product       |
| PUT    | `/products/{id}`        | Update product       |
| DELETE | `/products/{id}`        | Delete product       |

---

# Notes
- SKUs are normalized to lowercase for uniqueness.
- CSV processing is asynchronous and chunked for performance.
- Task progress is stored in Redis.
- Supports large CSV files (~500k rows).
- Uploads use streaming to avoid memory spikes.

---

# Commands Summary

### Environment
```
source venv/bin/activate
```

### Run API
```
uvicorn app.main:app --reload
```

### Run Worker
```
celery -A app.celery_app.celery worker --loglevel=info
```

### DB Migrations
```
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---
