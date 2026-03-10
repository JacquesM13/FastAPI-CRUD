from fastapi import APIRouter, HTTPException
from app.schemas import TaskCreate
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter()

@router.post("/tasks")
def create(task: TaskCreate):
    return create_task(task)


@router.get("/tasks")
def read_tasks():
    return get_tasks()


@router.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}")
def update(task_id: int, task: TaskCreate):
    updated = update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}")
def delete(task_id: int):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}