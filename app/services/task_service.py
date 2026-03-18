from sqlalchemy.orm import Session
from app import models, schemas


def create_task(db: Session, task: schemas.TaskCreate):
    """Create a new task"""
    db_task = models.Task(
        title=task.title,
        completed=task.completed
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session):
    """Return all tasks"""
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    """Return a single task by ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    """Update an existing task"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    db_task.title = task_update.title
    db_task.completed = task_update.completed

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    """Delete a task"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return db_task