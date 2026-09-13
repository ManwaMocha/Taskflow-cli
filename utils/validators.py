"""Validation helpers for Taskflow."""


VALID_STATUSES = {
    "todo",
    "in_progress",
    "completed",
}

VALID_PRIORITIES = {
    "low",
    "medium",
    "high",
}


def validate_status(status):
    """Validate a task status."""
    if status not in VALID_STATUSES:
        raise ValueError(
            "Invalid status. Choose todo, in_progress, or completed."
        )

    return True


def validate_priority(priority):
    """Validate a task priority."""
    if priority not in VALID_PRIORITIES:
        raise ValueError(
            "Invalid priority. Choose low, medium, or high."
        )

    return True


def validate_required(value, field_name):
    """Validate that a required value is provided."""
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} is required.")

    return True