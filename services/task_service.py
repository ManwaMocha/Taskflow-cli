"""Task business logic."""

from models.task import Task


class TaskService:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create(
        self,
        title,
        description,
        project_id,
        created_by,
        assigned_to=None,
        priority="medium",
        due_date=None,
    ):
        task = Task(
            self.task_storage.next_id(),
            title,
            description,
            project_id,
            created_by,
            assigned_to,
            priority=priority,
            due_date=due_date,
        )

        self.task_storage.add(task.to_dict())

        return task

    def list_all(self):
        return [
            Task.from_dict(item)
            for item in self.task_storage.load()
        ]

    def get(self, task_id):
        record = self.task_storage.find_by_id(task_id)

        return Task.from_dict(record) if record else None

    def list_for_user(self, user_id):
        return [
            task
            for task in self.list_all()
            if task.assigned_to == user_id
        ]

    def update_status(self, task_id, status):
        task = self.get(task_id)

        if not task:
            raise ValueError("Task not found.")

        task.update_status(status)

        self.task_storage.update(
            task.id,
            task.to_dict()
        )

        return task

    def delete(self, task_id):
        return self.task_storage.delete(task_id)