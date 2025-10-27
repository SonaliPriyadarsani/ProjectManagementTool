from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, db

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(db.get_db)):
    return crud.create_project(db, project)

@router.get("/", response_model=list[schemas.ProjectResponse])
def list_projects(db: Session = Depends(db.get_db)):
    return crud.get_projects(db)
