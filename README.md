# TaskFlow CLI

TaskFlow is a Python command-line application for managing team projects,
assigning tasks, tracking progress and discussing work through comments.

It provides registration, login, Admin and Member roles, and persistent
storage using JSON files.

## Team Members

| Member | Name | Responsibilities |
|---|---|---|
| 1 — Group Leader | Augustus Mocha | User models, authentication, decorators, CLI integration, tests, README and PR reviews/merges |
| 2 | Maureen Mutua | Project model, project service and project membership |
| 3 | Levis Nelson | Task model, task service and validation |
| 4 | Stanley Ngunijiri | Comment model, comment service and reusable JSON storage |

## Problem Statement

Teams need a shared way to organize projects, assign responsibilities and
track task progress. TaskFlow provides these features through an interactive
terminal interface and saves information between sessions.

## Features

- Register and log in with bcrypt password hashing.
- First registered account becomes Admin; later accounts become Members.
- Create, view and delete projects.
- Add and remove project members.
- Update project status.
- Create, assign and delete tasks.
- Update task status and priority.
- Validate task due dates.
- Add and view task comments.
- Restrict actions according to the logged-in user's role.
- Save records in JSON files.
- Log successful decorated actions.

Admins can manage all projects and tasks. Members can view their projects,
access tasks assigned to them, update task status and leave comments.

## Requirements

- Python 3.10 or newer.
- Git.
- Dependencies listed in `requirements.txt`.

The project has been developed using Python 3.12. The supplied Pipfile
specifies Python 3.12.

## Installation

Clone the repository:

```bash
git clone https://github.com/ManwaMocha/Taskflow-cli.git
cd Taskflow-cli
```

Create and activate a virtual environment on Linux, WSL or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start the menus:

```bash
python main.py
```

Or use the interactive subcommand:

```bash
python main.py interactive
```

View command-line help:

```bash
python main.py --help
python main.py interactive --help
```

Use a separate folder for manual testing:

```bash
python main.py interactive --data-dir manual-test-data
```

Restart with the same data folder to reuse its saved accounts and records.
The first registration becomes Admin only when that folder's users file
contains no accounts.

Passwords are hidden while typing.

## Example Workflow

1. Register the first account, which becomes Admin.
2. Register another account, which becomes Member.
3. Log in as Admin.
4. Create a project.
5. Add the Member to the project.
6. Create a task and assign it to that Member.
7. Log out and log in as Member.
8. View the assigned task and update its status.
9. Add a comment.
10. Restart the application to check persistence.

Task dates use `YYYY-MM-DD`, for example `2026-09-30`.

Project statuses: `active`, `completed`, `archived`.

Task statuses: `pending`, `in progress`, `completed`.

Task priorities: `low`, `medium`, `high`.

## Project Structure

```text
Taskflow-cli/
├── main.py
├── cli/
│   ├── __init__.py
│   └── app.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── project.py
│   ├── task.py
│   └── comment.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── project_service.py
│   ├── task_service.py
│   └── comment_service.py
├── storage/
│   ├── __init__.py
│   └── json_storage.py
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   └── validators.py
├── data/
│   ├── users.json
│   ├── projects.json
│   ├── tasks.json
│   └── comments.json
├── tests/
│   ├── test_auth_service.py
│   └── test_decorators.py
├── requirements.txt
├── Pipfile
└── README.md
```

## Architecture and OOP

- **Classes and objects:** User, Project, Task and Comment represent records.
- **Inheritance:** Admin and Member inherit from User.
- **Encapsulation:** User stores its password hash in `__password_hash`
  and exposes a read-only property.
- **Polymorphism:** `can_manage_users()` behaves differently for Admin
  and Member objects.
- **Services:** Authentication and entity operations are separated from models.
- **Dependency injection:** Storage is passed into services, and services
  are passed into CLIApp.
- **Decorators:** `login_required`, `role_required` and `log_action`
  provide reusable access checks and logging.

Role permissions are enforced in the CLI. Service methods are internal
application components and do not independently authenticate callers.

## JSON Persistence

Each entity has a separate JSON file.

- `to_dict()` converts model objects into dictionaries.
- JsonStorage reads and writes those dictionaries.
- `from_dict()` rebuilds model objects.
- IDs connect users, projects, tasks and comments.
- Invalid JSON or storage read failures raise errors instead of being
  treated as empty data.

Deleting a task also removes its comments. Deleting a project removes its
tasks and their comments.

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

The current 13 automated tests cover:

- Admin and Member registration.
- Password hashing.
- Successful and unsuccessful login.
- Duplicate username rejection.
- User listing and lookup.
- Login and role restrictions.
- Action logging.

These tests do not provide complete CLI coverage. The example workflow
above should also be tested manually, including invalid inputs and
persistence after restarting.

## Dependencies

- **bcrypt:** Password hashing and verification.
- **pytest:** Automated testing.

`requirements.txt` supports installation with pip. `Pipfile` declares
application and development dependencies for Pipenv.

## Collaboration

Each member works on a feature branch and submits pull requests into `main`.
The leader reviews changes, coordinates corrections and merges the work.
Integration is developed on `feature/cli-integration`.

Trello is used to assign tasks and track progress through development,
review, testing and completion.

## Known Limitations

- Intended for a small local CLI demonstration, not a production service.
- JSON writes are not transactional or protected against simultaneous users.
- Multi-file deletion may be partially completed if a storage error occurs.
- No password reset or account recovery.
- No complete automated coverage of interactive menus.
- Due dates accept calendar dates in `YYYY-MM-DD` format.

## Future Improvements

- Add integration and CLI tests.
- Replace JSON with a transactional database.
- Add password reset and stronger account-management controls.
- Add task search, reports and reminders.

## Project Management

We used Trello to assign responsibilities and track progress.

[View our Trello board](https://trello.com/b/PVdFgDFs)