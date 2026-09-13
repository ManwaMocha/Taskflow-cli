"""Comment model."""

from datetime import datetime, timezone


class Comment:
    def __init__(self, comment_id, task_id, user_id, message, created_at=None):
        if not message.strip():
            raise ValueError("Comment cannot be empty.")

        self.id = comment_id
        self.task_id = task_id
        self.user_id = user_id
        self.message = message.strip()
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["task_id"],
            data["user_id"],
            data["message"],
            data.get("created_at"),
        )