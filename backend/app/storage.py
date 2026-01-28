from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.models import ActivityLog, Task, TaskStats


class Storage:
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.activity_logs: dict[str, list[ActivityLog]] = {}
        self.deleted_activity_logs: dict[str, list[ActivityLog]] = {}

    def _add_activity_log(
        self,
        task_id: str,
        action: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> None:
        log = ActivityLog(
            id=str(uuid4()),
            task_id=task_id,
            action=action,
            timestamp=datetime.utcnow(),
            old_value=old_value,
            new_value=new_value,
        )
        if task_id not in self.activity_logs:
            self.activity_logs[task_id] = []
        self.activity_logs[task_id].append(log)

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def create_task(self, title: str) -> Task:
        task_id = str(uuid4())
        now = datetime.utcnow()
        task = Task(
            id=task_id,
            title=title,
            completed=False,
            created_at=now,
            updated_at=now,
        )
        self.tasks[task_id] = task
        self._add_activity_log(task_id, "created")
        return task

    def complete_task(self, task_id: str) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        old_status = "completed" if task.completed else "pending"
        updated_task = task.model_copy(
            update={"completed": True, "updated_at": datetime.utcnow()}
        )
        self.tasks[task_id] = updated_task
        self._add_activity_log(task_id, "completed", old_value=old_status, new_value="completed")
        return updated_task

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if task is None:
            return None

        updates = {"updated_at": datetime.utcnow()}

        if title is not None and title != task.title:
            old_title = task.title
            updates["title"] = title
            self._add_activity_log(task_id, "updated", old_value=old_title, new_value=title)

        if completed is not None and completed != task.completed:
            old_status = "completed" if task.completed else "pending"
            new_status = "completed" if completed else "pending"
            updates["completed"] = completed
            self._add_activity_log(task_id, "status_changed", old_value=old_status, new_value=new_status)

        updated_task = task.model_copy(update=updates)
        self.tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False
        self._add_activity_log(task_id, "deleted")
        # Archive activity logs before deleting
        if task_id in self.activity_logs:
            self.deleted_activity_logs[task_id] = self.activity_logs.pop(task_id)
        del self.tasks[task_id]
        return True

    def get_task_activity(self, task_id: str) -> Optional[list[ActivityLog]]:
        if task_id not in self.tasks:
            return None
        return self.activity_logs.get(task_id, [])

    def get_stats(self) -> TaskStats:
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks.values() if task.completed)
        pending = total - completed
        return TaskStats(total=total, completed=completed, pending=pending)

    def clear(self) -> None:
        """Clear all data - useful for testing."""
        self.tasks.clear()
        self.activity_logs.clear()
        self.deleted_activity_logs.clear()


# Global storage instance
storage = Storage()
