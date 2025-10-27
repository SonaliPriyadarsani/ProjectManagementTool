from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import date

# ----------------------------------
# ✅ User Schemas
# ----------------------------------

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.developer


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True  # ✅ updated for Pydantic v2


# ----------------------------------
# ✅ Project Schemas
# ----------------------------------

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        from_attributes = True


# ----------------------------------
# ✅ Task Schemas
# ----------------------------------

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    assignee_id: int
    deadline: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    project_id: int
    assignee_id: int
    status: Optional[str]
    deadline: Optional[date]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
