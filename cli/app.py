"""Interactive command-line interface."""

from getpass import getpass
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
            print("\n--- TaskFlow CLI ---")
            print("1. Register")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    self.register_user()
                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Choose 1 or 0.")
            except (ValueError, RuntimeError) as error:
                print(f"Error: {error}")

    def register_user(self):
        username = input("Username: ")
        password = getpass("Password: ")

        user = self.auth_service.register(username, password)

        print(
            f"Account created for {user.username}. "
            f"Role: {user.role}"
        )