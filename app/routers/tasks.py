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
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Enforce ownership
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    return task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int,
                task: schemas.TaskUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    """
    Update an existing task
    """
    # Enforce ownership
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")
    updated_task = task_service.update_task(db, task_id, task)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Enforce ownership
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    return task