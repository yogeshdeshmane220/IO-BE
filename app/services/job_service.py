from app.repositories.job_repository import JobRepository

class JobService:
    def __init__(self, db):
        self.repo = JobRepository(db)

    def start_job(self):
        return self.repo.create(status="uploading", phase="receiving_file")

    def update(self, job_id, **fields):
        return self.repo.update(job_id, **fields)

    def get(self, job_id):
        return self.repo.get(job_id)
