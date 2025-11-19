from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.job_service import JobService
from app.workers.tasks import process_csv
import os

router = APIRouter(prefix="/upload")

@router.post("/")
def start_upload(file: UploadFile = File(...), db: Session = Depends(get_session)):
    svc = JobService(db)
    job = svc.start_job()

    # ----------- NEW SHARED UPLOAD DIRECTORY -----------
    upload_dir = os.getenv("UPLOAD_DIR", "/shared")
    os.makedirs(upload_dir, exist_ok=True)

    temp_path = os.path.join(upload_dir, f"upload_{job.id}.csv")
    # -----------------------------------------------------

    # save file to shared directory
    with open(temp_path, "wb") as f:
        for chunk in iter(lambda: file.file.read(1024 * 1024), b""):
            f.write(chunk)

    # send to celery
    process_csv.delay(job.id, temp_path)

    return {"job_id": job.id}

@router.get("/{job_id}")
def get_status(job_id: int, db: Session = Depends(get_session)):
    svc = JobService(db)
    job = svc.get(job_id)
    return {
        "id": job.id,
        "status": job.status,
        "phase": job.phase,
        "percent": job.percent,
        "error_message": job.error_message,
    }
