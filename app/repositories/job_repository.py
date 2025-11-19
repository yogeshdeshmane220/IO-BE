from sqlalchemy.orm import Session
from app.models.job import Job

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, status, phase):
        job = Job(status=status, phase=phase, percent=0.0)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job_id, **fields):
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        for k, v in fields.items():
            setattr(job, k, v)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id):
        return self.db.query(Job).filter(Job.id == job_id).first()
