"""Task model."""

from datetime import datetime, timezone


class Task:
    VALID_STATUSES = {"pending", "in progress", "completed"}
    VALID_PRIORITIES = {"low", "medium", "high"}

    def __init__(
        self,
        task_id,
        title,
        description,
        project_id,
        created_by,
        assigned_to=None,
        status="pending",
        priority="medium",
        due_date=None,
        created_at=None,
    ):
        if not title.strip():
            raise ValueError("Task title cannot be empty.")

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid task status.")

        if priority not in self.VALID_PRIORITIES:
            raise ValueError("Priority must be low, medium, or high.")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.project_id = project_id
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def assign_to(self, user_id):
        self.assigned_to = user_id

    def update_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Status must be pending, in progress, or completed."
            )

        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "project_id": self.project_id,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data.get("description", ""),
            data["project_id"],
            data["created_by"],
            data.get("assigned_to"),
            data.get("status", "pending"),
            data.get("priority", "medium"),
            data.get("due_date"),
            data.get("created_at"),
        )