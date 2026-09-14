"""Entry point for TaskFlow CLI."""

from pathlib import Path

from cli.app import CLIApp
from storage.json_storage import JsonStorage
from services.auth_service import AuthService
from services.project_service import ProjectService
from services.task_service import TaskService
from services.comment_service import CommentService


def create_app():
    data_folder = Path(__file__).resolve().parent / "data"

    user_storage = JsonStorage(data_folder / "users.json")
    project_storage = JsonStorage(data_folder / "projects.json")
    task_storage = JsonStorage(data_folder / "tasks.json")
    comment_storage = JsonStorage(data_folder / "comments.json")

    auth_service = AuthService(user_storage)
    project_service = ProjectService(project_storage)
    task_service = TaskService(task_storage)
    comment_service = CommentService(comment_storage)

    return CLIApp(
        auth_service,
        project_service,
        task_service,
        comment_service,
    )