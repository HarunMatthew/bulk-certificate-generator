from pydantic import BaseModel, EmailStr, Field
from typing import List


class Recipient(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class JobCreate(BaseModel):
    event_name: str = Field(..., min_length=1)
    date: str
    recipients: List[Recipient] = Field(..., min_length=1)
