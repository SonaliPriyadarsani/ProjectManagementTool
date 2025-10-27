from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, db, auth
from ..models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ✅ Get the current logged-in user
def get_current_user(token: str = Depends(auth.oauth2_scheme), db_session: Session = Depends(db.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db_session.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# ✅ Managers & Admins → Can create tasks
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db_session: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Only managers or admins can create tasks")

    return crud.create_task(db_session, task)


# ✅ Get all tasks depending on user role
@router.get("/", response_model=List[schemas.TaskResponse])
def get_all_tasks(
    db_session: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user)
):
    # Developer → see only their own tasks
    if current_user.role == "developer":
        return crud.get_tasks_by_assignee(db_session, current_user.id)
    # Manager/Admin → see all tasks
    elif current_user.role in ["manager", "admin"]:
        return crud.get_tasks(db_session)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view tasks")
