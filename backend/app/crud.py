# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import List, Optional

# -------------------------------------------------
# USER OPERATIONS
# -------------------------------------------------

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user with hashed password"""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    """Fetch a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session):
    """Fetch all users"""
    return db.query(models.User).all()


# -------------------------------------------------
# PROJECT OPERATIONS
# -------------------------------------------------

def create_project(db: Session, project: schemas.ProjectCreate, created_by: int):
    """Create a new project"""
    db_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=created_by,
        start_date=project.start_date,
        end_date=project.end_date
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_all_projects(db: Session):
    """Return all projects"""
    return db.query(models.Project).all()


def get_project_by_id(db: Session, project_id: int):
    """Return a project by ID"""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


# -------------------------------------------------
# TASK OPERATIONS
# -------------------------------------------------

def create_task(db: Session, task: schemas.TaskCreate):
    """Create a new task (Managers only)"""
    db_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assignee_id=task.assignee_id,
        deadline=task.deadline,
        status=task.status
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session) -> List[models.Task]:
    """Return all tasks (Managers/Admins)"""
    return db.query(models.Task).all()


def get_tasks_by_assignee(db: Session, assignee_id: int) -> List[models.Task]:
    """Return tasks assigned to a specific developer"""
    return db.query(models.Task).filter(models.Task.assignee_id == assignee_id).all()


def get_tasks_by_project(db: Session, project_id: int):
    """Return all tasks for a specific project"""
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def update_task_status(db: Session, task_id: int, status: str):
    """Update the status of a task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Delete a task (Managers only)"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
