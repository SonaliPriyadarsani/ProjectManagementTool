from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from .db import Base
import enum

# ---------------------------------
# Enums
# ---------------------------------
class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"

# ---------------------------------
# User Table
# ---------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.developer)

    # Relationships
    projects = relationship("Project", back_populates="creator")
    tasks = relationship("Task", back_populates="assignee")

# ---------------------------------
# Project Table
# ---------------------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

# ---------------------------------
# Task Table
# ---------------------------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="todo")
    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(Date)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
