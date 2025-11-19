# **Acme Backend — FastAPI + PostgreSQL + Celery + Redis**

This backend provides:

- CSV ingestion (up to 500k rows)
- Background processing using Celery
- Deduped product merging (case-insensitive SKU)
- Product CRUD
- Webhook management
- Real-time job tracking
- Dockerized local environment

---

# **1. Requirements**

Install:

- Docker  
- Docker Compose  
- Git  

Nothing else is required.

---

# **2. Clone the Repository**

```bash
git clone <REPO_URL>
cd backend
```

---

# **3. Environment Variables**

Create a `.env` file in the backend root:

```
DATABASE_URL=postgresql://acme:acme@db:5432/acme
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_BACKEND_URL=redis://redis:6379/0
UPLOAD_DIR=/shared
```

No additional configuration needed.

---

# **4. Start the Full Stack**

Start API + Worker + Postgres + Redis:

```bash
docker-compose up --build
```

App runs at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

# **5. Run Database Migrations**

Enter the API container:

```bash
docker exec -it acme-api bash
```

Run migrations:

```bash
alembic upgrade head
```

---

# **6. Project Structure**

```
app/
  api/
    upload.py
    products.py
    webhooks.py
  db/
    db.py
    session.py
  models/
    product.py
    product_staging.py
    job.py
    webhook.py
  services/
    job_service.py
    product_service.py
  workers/
    celery_app.py
    tasks.py
migrations/
docker-compose.yml
Dockerfile
```

---

# **7. CSV Ingestion Flow**

1. Upload CSV → `/upload/`  
2. API saves file, creates job  
3. Celery worker processes CSV  
4. Dedupes rows (lowercase SKU)  
5. Bulk upsert into `products`  
6. Job updated with progress  
7. Frontend polls `/upload/{job_id}`  

---

# **8. Run Celery Worker Manually (optional)**

```bash
docker exec -it acme-worker bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

---

# **9. Reset Database**

```bash
docker-compose down -v
docker-compose up --build
alembic upgrade head
```

---

# **10. Quick API Tests**

Get all products:

```bash
curl http://localhost:8000/products
```

Upload CSV:

```bash
curl -F "file=@products.csv" http://localhost:8000/upload/
```

---

# **11. Troubleshooting**

### **API can't connect to DB**
DB starts slower than API. Run:

```bash
docker-compose up --build
```

### **Missing tables**
Run migrations:

```bash
docker exec -it acme-api alembic upgrade head
```

---

# **Developer Onboarding Summary**

1. Clone repo  
2. `docker-compose up --build`  
3. `alembic upgrade head`  
4. Visit `http://localhost:8000/docs`  
5. Start building  

---
