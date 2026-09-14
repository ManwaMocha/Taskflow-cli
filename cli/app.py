"""Interactive menus for TaskFlow CLI."""

from getpass import getpass

from utils.decorators import login_required, role_required, log_action


class CLIApp:
    def __init__(
        self,
        auth_service,
        project_service,
        task_service,
        comment_service,
    ):
        self.auth_service = auth_service
        self.project_service = project_service
        self.task_service = task_service
        self.comment_service = comment_service
        self.current_user = None

    def run(self):
        while True:
            try:
                print("\n--- TaskFlow CLI ---")

                if self.current_user is None:
                    print("1. Register")
                    print("2. Login")
                    actions = {
                        "1": self.register_user,
                        "2": self.login_user,
                    }
                else:
                    print(
                        f"User: {self.current_user.username} "
                        f"({self.current_user.role})"
                    )
                    print("3. Logout")
                    print("5. View projects")
                    print("8. View tasks")
                    print("9. Update task status")
                    print("10. Add comment")
                    print("11. View comments")

                    actions = {
                        "3": self.logout_user,
                        "5": self.view_projects,
                        "8": self.view_tasks,
                        "9": self.update_task_status,
                        "10": self.add_comment,
                        "11": self.view_comments,
                    }

                    if self.current_user.role == "admin":
                        print("4. Create project")
                        print("6. Add member to project")
                        print("7. Create task")
                        print("12. List users")
                        print("13. Assign task")
                        print("14. Change task priority")
                        print("15. Change project status")
                        print("16. Remove project member")
                        print("17. Delete task")
                        print("18. Delete project")

                        actions.update({
                            "4": self.create_project,
                            "6": self.add_project_member,
                            "7": self.create_task,
                            "12": self.list_users,
                            "13": self.assign_task,
                            "14": self.change_task_priority,
                            "15": self.change_project_status,
                            "16": self.remove_project_member,
                            "17": self.delete_task,
                            "18": self.delete_project,
                        })

                print("0. Exit")
                choice = input("Choose an option: ").strip()

                if choice == "0":
                    print("Goodbye!")
                    break

                action = actions.get(choice)

                if action is None:
                    print("Invalid option.")
                else:
                    action()

            except (ValueError, RuntimeError, PermissionError) as error:
                print(f"Error: {error}")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

    def read_id(self, prompt):
        try:
            value = int(input(prompt).strip())
        except ValueError:
            raise ValueError("Enter a whole-number ID.")

        if value < 1:
            raise ValueError("ID must be greater than zero.")

        return value

    def get_project(self, project_id):
        project = self.project_service.get(project_id)

        if project is None:
            raise ValueError("Project not found.")

        return project

    def get_accessible_task(self, task_id):
        if self.current_user is None:
            raise PermissionError("You must log in first.")

        task = self.task_service.get(task_id)

        if task is None:
            raise ValueError("Task not found.")

        project = self.get_project(task.project_id)

        if self.current_user.role != "admin":
            if (
                task.assigned_to != self.current_user.id
                or self.current_user.id not in project.member_ids
            ):
                raise PermissionError("You cannot access this task.")

        return task

    def get_project_member(self, project, user_id):
        user = self.auth_service.get_user(user_id)

        if user is None or user.role != "member":
            raise ValueError("Enter a valid Member account ID.")

        if user_id not in project.member_ids:
            raise ValueError("Add this member to the project first.")

        return user

    def register_user(self):
        username = input("Username: ")
        password = getpass("Password: ")

        user = self.auth_service.register(username, password)

        print(
            f"Account created: {user.username} ({user.role}). "
            "Choose Login to sign in."
        )

    def login_user(self):
        username = input("Username: ")
        password = getpass("Password: ")

        user = self.auth_service.login(username, password)

        if user is None:
            print("Incorrect username or password.")
            return

        self.current_user = user
        print(f"Welcome, {user.username}!")

    @login_required
    def logout_user(self):
        self.current_user = None
        print("Logged out.")

    @role_required("admin")
    def list_users(self):
        for user in self.auth_service.list_users():
            print(
                f"ID: {user.id} | "
                f"Username: {user.username} | Role: {user.role}"
            )

    @login_required
    def view_projects(self):
        projects = self.project_service.list_all()

        if self.current_user.role != "admin":
            projects = [
                project
                for project in projects
                if self.current_user.id in project.member_ids
            ]

        if not projects:
            print("No projects available.")
            return

        for project in projects:
            print(
                f"\nID: {project.id} | {project.name} | "
                f"Status: {project.status}\n"
                f"Description: {project.description}\n"
                f"Member IDs: {project.member_ids}"
            )

    @role_required("admin")
    @log_action
    def create_project(self):
        name = input("Project name: ")
        description = input("Description: ")

        project = self.project_service.create(
            name, description, self.current_user.id
        )

        print(f"Created project {project.id}: {project.name}")

    @role_required("admin")
    @log_action
    def add_project_member(self):
        self.view_projects()
        project = self.get_project(self.read_id("Project ID: "))

        self.list_users()
        user_id = self.read_id("Member ID: ")
        user = self.auth_service.get_user(user_id)

        if user is None or user.role != "member":
            raise ValueError("Enter a valid Member account ID.")

        if user_id in project.member_ids:
            print("This member already belongs to the project.")
            return

        self.project_service.add_member(project.id, user_id)
        print(f"{user.username} added to {project.name}.")

    @role_required("admin")
    @log_action
    def remove_project_member(self):
        self.view_projects()
        project = self.get_project(self.read_id("Project ID: "))
        user_id = self.read_id("Member ID to remove: ")
        self.get_project_member(project, user_id)

        # Prevent assignments from pointing to someone outside the project.
        for task in self.task_service.list_all():
            if task.project_id == project.id and task.assigned_to == user_id:
                raise ValueError(
                    "Reassign or delete this member's project tasks first."
                )

        project.remove_member(user_id)
        self.project_service.project_storage.update(
            project.id, project.to_dict()
        )
        print("Member removed.")

    @role_required("admin")
    @log_action
    def change_project_status(self):
        self.view_projects()
        project = self.get_project(self.read_id("Project ID: "))

        status = input(
            "Status (active/completed/archived): "
        ).strip().lower()

        project.update_status(status)
        self.project_service.project_storage.update(
            project.id, project.to_dict()
        )
        print("Project status updated.")

    @role_required("admin")
    @log_action
    def create_task(self):
        self.view_projects()
        project = self.get_project(self.read_id("Project ID: "))

        if project.status != "active":
            raise ValueError("Create tasks only in active projects.")

        self.list_users()
        user_id = self.read_id("Assign to Member ID: ")
        self.get_project_member(project, user_id)

        title = input("Task title: ")
        description = input("Description: ")
        priority = input(
            "Priority (low/medium/high) [medium]: "
        ).strip().lower() or "medium"
        due_date = input(
            "Due date (YYYY-MM-DD, blank for none): "
        ).strip() or None

        task = self.task_service.create(
            title=title,
            description=description,
            project_id=project.id,
            created_by=self.current_user.id,
            assigned_to=user_id,
            priority=priority,
            due_date=due_date,
        )

        print(f"Created task {task.id}: {task.title}")

    @login_required
    def view_tasks(self):
        if self.current_user.role == "admin":
            tasks = self.task_service.list_all()
        else:
            project_ids = {
                project.id
                for project in self.project_service.list_all()
                if self.current_user.id in project.member_ids
            }
            tasks = [
                task
                for task in self.task_service.list_for_user(
                    self.current_user.id
                )
                if task.project_id in project_ids
            ]

        if not tasks:
            print("No tasks available.")
            return

        for task in tasks:
            print(
                f"\nID: {task.id} | {task.title}\n"
                f"Project: {task.project_id} | "
                f"Assigned to: {task.assigned_to}\n"
                f"Status: {task.status} | Priority: {task.priority}\n"
                f"Due: {task.due_date or 'None'}\n"
                f"Description: {task.description}"
            )

    @login_required
    @log_action
    def update_task_status(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))

        status = input(
            "Status (pending/in progress/completed): "
        ).strip().lower()

        self.task_service.update_status(task.id, status)
        print("Task status updated.")

    @role_required("admin")
    @log_action
    def assign_task(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))
        project = self.get_project(task.project_id)

        self.list_users()
        user_id = self.read_id("New Member ID: ")
        self.get_project_member(project, user_id)

        task.assign_to(user_id)
        self.task_service.task_storage.update(task.id, task.to_dict())
        print("Task assignment updated.")

    @role_required("admin")
    @log_action
    def change_task_priority(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))

        priority = input(
            "Priority (low/medium/high): "
        ).strip().lower()

        if priority not in task.VALID_PRIORITIES:
            raise ValueError("Priority must be low, medium, or high.")

        task.priority = priority
        self.task_service.task_storage.update(task.id, task.to_dict())
        print("Task priority updated.")

    @login_required
    @log_action
    def add_comment(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))
        message = input("Comment: ")

        comment = self.comment_service.create(
            task.id, self.current_user.id, message
        )
        print(f"Comment {comment.id} added.")

    @login_required
    def view_comments(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))
        comments = self.comment_service.list_for_task(task.id)

        if not comments:
            print("No comments for this task.")
            return

        for comment in comments:
            author = self.auth_service.get_user(comment.user_id)
            username = author.username if author else "Unknown user"

            print(
                f"\n{username} | {comment.created_at}\n"
                f"{comment.message}"
            )

    def delete_task_records(self, task_id):
        # Remove comments before deleting their parent task.
        for comment in self.comment_service.list_for_task(task_id):
            self.comment_service.comment_storage.delete(comment.id)

        self.task_service.delete(task_id)

    @role_required("admin")
    @log_action
    def delete_task(self):
        self.view_tasks()
        task = self.get_accessible_task(self.read_id("Task ID: "))

        confirmation = input(
            f"Delete '{task.title}' and its comments? Type yes: "
        ).strip().lower()

        if confirmation != "yes":
            print("Cancelled.")
            return

        self.delete_task_records(task.id)
        print("Task and its comments deleted.")

    @role_required("admin")
    @log_action
    def delete_project(self):
        self.view_projects()
        project = self.get_project(self.read_id("Project ID: "))

        confirmation = input(
            f"Delete '{project.name}', its tasks and comments? Type yes: "
        ).strip().lower()

        if confirmation != "yes":
            print("Cancelled.")
            return

        for task in self.task_service.list_all():
            if task.project_id == project.id:
                self.delete_task_records(task.id)

        self.project_service.delete(project.id)
        print("Project, tasks and comments deleted.")