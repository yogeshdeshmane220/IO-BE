from pydantic import BaseModel

class WebhookBase(BaseModel):
    url: str
    event_type: str
    enabled: bool = True

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(BaseModel):
    url: str | None = None
    event_type: str | None = None
    enabled: bool | None = None

class WebhookOut(WebhookBase):
    id: int
    class Config:
        orm_mode = True
