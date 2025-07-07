# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class CollectionCreate(BaseModel):
    hostname: str
    system: Optional[str] = None
    file_name: str
    file_path: str
    uploaded_to_drive: bool = False
    drive_url: Optional[str] = None
    error_count: int = 0

class CollectionResponse(BaseModel):
    id: int
    user_id: int
    hostname: str
    system: str
    collection_date: datetime
    file_name: str
    file_path: str
    uploaded_to_drive: bool
    drive_url: Optional[str]
    error_count: int

    class Config:
        orm_mode = True
