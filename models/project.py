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
        




        