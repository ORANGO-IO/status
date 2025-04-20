from pydantic import BaseModel
from typing import Optional, Any, List, Dict
from datetime import datetime


class TaskResultSchema(BaseModel):
    id: str
    status: str
    output: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: str
    name: str
    type: str
    active: bool
    last_status: Optional[str]
    last_ran_at: Optional[datetime]
    config: Optional[Any]
    service_id: str
    results: Optional[List[TaskResultSchema]] = []

    class Config:
        from_attributes = True  # importante para usar com SQLAlchemy
