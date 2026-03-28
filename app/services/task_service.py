from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy import select, func



def create_task(db: Session, task_data: schemas.TaskCreate, user_id: int):
    """Create a new task"""

    title = task_data.title.strip()

    existing_task = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        func.lower(models.Task.title) == title.lower()
    ).first()

    if existing_task:
        raise HTTPException(
            status_code=400,
            detail="Task with this title already exists"
        )

    new_task = models.Task(
        title=title,
        completed=task_data.completed,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db: Session, user_id: int):
    stmt = select(models.Task).where(models.Task.user_id == user_id)
    return db.execute(stmt).scalars().all()


def get_task(db: Session, task_id: int, user_id: int):
    """Return a single task by ID"""
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task

def update_task(db: Session, old_task: int, task_data: schemas.TaskUpdate, user_id: int):
    """Update an existing task"""
    task = db.get(models.Task, old_task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int, user_id: int):
    """Delete a task"""
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(task)
    db.commit()
    return task