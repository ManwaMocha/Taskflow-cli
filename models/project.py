from datetime import datetime, timezone

class Project:
    VALID_STATUSES = {"active", "completed", "archived"}

    def __init__(
        self, 
        project_id, 
        name, 
        description, 
        created_by, 
        member_ids=None,
        status="active", 
        created_at=None,
    ):
        if not name.strip():
            raise ValueError("Project name cannot be empty.")

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid project status.")

        self.id = project_id
        self.name = name.strip()
        self.description = description.strip()
        self.created_by = created_by
        self.member_ids = member_ids or []
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    def add_member(self, user_id):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)

    def remove_member(self, user_id):
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)

    def update_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Status must be active, completed or archived")
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "member_ids": self.member_ids,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data.get("description", ""),
            data["created_by"],
            data.get("member_ids", []),
            data.get("status", "active"),
            data.get("created_at")
        )





        