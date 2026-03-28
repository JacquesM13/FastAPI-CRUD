from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, models
from app.services import task_service

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=schemas.Task)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.create_task(db, task_data, current_user.id)



@router.get("/", response_model=list[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.get_tasks(db, current_user.id)


@router.get("/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.get_task(db, task_id, current_user.id)


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int,
                task_data: schemas.TaskUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    """
    Update an existing task
    """
    return task_service.update_task(db, task_id, task_data, current_user.id)


@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.delete_task(db, task_id, current_user.id)