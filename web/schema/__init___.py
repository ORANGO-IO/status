from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class TaskSchema(BaseModel):
    id: str
    name: str
    type: str
    active: bool
    last_status: Optional[str]
    last_ran_at: Optional[datetime]
    config: Optional[Any]
    service_id: str

    class Config:
        from_attributes = True  # importante para usar com SQLAlchemy