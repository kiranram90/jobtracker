from pydantic import BaseModel
from datetime import datetime


class JobApplicationDTO(BaseModel):
    id: str
    company_name: str
    position: str
    status: str
    notes: str
    created_at: datetime