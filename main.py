"""Start TaskFlow and handle command-line arguments."""

import argparse
import logging
from pathlib import Path

from cli.app import CLIApp
from storage.json_storage import JsonStorage
from services.auth_service import AuthService
from services.project_service import ProjectService
from services.task_service import TaskService
from services.comment_service import CommentService


DEFAULT_DATA_FOLDER = Path(__file__).resolve().parent / "data"


def create_app(data_folder):
    data_folder = Path(data_folder)

    user_storage = JsonStorage(data_folder / "users.json")
    project_storage = JsonStorage(data_folder / "projects.json")
    task_storage = JsonStorage(data_folder / "tasks.json")
    comment_storage = JsonStorage(data_folder / "comments.json")

    return CLIApp(
        AuthService(user_storage),
        ProjectService(project_storage),
        TaskService(task_storage),
        CommentService(comment_storage),
    )


def main():
    parser = argparse.ArgumentParser(
        description="TaskFlow: a Python project management CLI."
    )
    commands = parser.add_subparsers(dest="command")

    interactive = commands.add_parser(
        "interactive",
        help="Open the interactive registration and login menus.",
    )
    interactive.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_FOLDER,
        help="Folder for JSON data and the application log.",
    )

    args = parser.parse_args()

    # Running without a subcommand also opens the menus.
    data_folder = (
        args.data_dir
        if args.command == "interactive"
        else DEFAULT_DATA_FOLDER
    )

    try:
        data_folder.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=str(data_folder / "taskflow.log"),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            encoding="utf-8",
        )

        app = create_app(data_folder)
        app.run()

    except (OSError, RuntimeError) as error:
        print(f"Could not start TaskFlow: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())