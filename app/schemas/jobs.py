from pydantic import BaseModel

class JobOut(BaseModel):
    id: int
    status: str
    phase: str
    percent: float
    error_message: str | None = None
    class Config:
        orm_mode = True
