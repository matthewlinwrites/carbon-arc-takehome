from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from app.models import ActivityLog, Task, TaskStats
from app.schemas import TaskCreate, TaskUpdate
from app.storage import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def list_tasks() -> list[Task]:
    return storage.get_all_tasks()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate) -> Task:
    return storage.create_task(task_create.title)


@router.get("/stats", response_model=TaskStats)
def get_stats() -> TaskStats:
    return storage.get_stats()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return task


@router.put("/{task_id}/complete", response_model=Task)
def complete_task(task_id: str) -> Task:
    task = storage.complete_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: str, update: TaskUpdate) -> Task:
    task = storage.update_task(task_id, title=update.title, completed=update.completed)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{task_id}/activity", response_model=list[ActivityLog])
def get_task_activity(task_id: str) -> list[ActivityLog]:
    activity = storage.get_task_activity(task_id)
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return activity
