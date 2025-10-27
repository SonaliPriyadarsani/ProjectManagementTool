# backend/app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, db, auth
from .auth import get_current_user
from .models import UserRole

# ------------------------------------------------------
# 🚀 Initialize app
# ------------------------------------------------------
app = FastAPI(title="🎯 Project Management API with Role-Based Access")

# ------------------------------------------------------
# 🌐 CORS configuration (for frontend)
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# 🧱 Database setup
# ------------------------------------------------------
models.Base.metadata.create_all(bind=db.engine)

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()


app.include_router(auth.router, tags=["Auth"])  

# ------------------------------------------------------
# 🧩 Root route (for testing)
# ------------------------------------------------------
@app.get("/")
def home():
    return {"message": "🎯 Project Management API is running successfully!"}


# ------------------------------------------------------
# 📁 Project Routes
# ------------------------------------------------------
@app.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ✅ Only Admin or Manager can create projects
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(status_code=403, detail="Not authorized to create a project.")
    
    return crud.create_project(db=db, project=project, created_by=current_user.id)


@app.get("/projects/", response_model=List[schemas.ProjectResponse])
def get_all_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ✅ Admin & Manager see all projects
    if current_user.role in [UserRole.admin, UserRole.manager]:
        return crud.get_all_projects(db)
    # ✅ Developer sees only their assigned projects (optional)
    return crud.get_all_projects(db)  # You can later filter for developer-specific

# ------------------------------------------------------
# ✅ Task Routes
# ------------------------------------------------------
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ✅ Only Admin or Manager can create tasks
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks.")
    
    return crud.create_task(db=db, task=task)


@app.get("/tasks/", response_model=List[schemas.TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ✅ Admin or Manager -> see all tasks
    if current_user.role in [UserRole.admin, UserRole.manager]:
        return crud.get_tasks(db)
    # ✅ Developer -> see only their own tasks
    return crud.get_tasks_by_assignee(db, current_user.id)

# ------------------------------------------------------
# 🧾 Simple protected route: current user info
# ------------------------------------------------------
@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }
