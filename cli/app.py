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

            if self.current_user is None:
                print("1. Register")
                print("2. Login")
            else:
                print(f"Logged in as: {self.current_user.username}")
                print(f"Role: {self.current_user.role}")
                print("3. Logout")

            print("0. Exit")
            choice = input("Choose an option: ").strip()

            try:
                if choice == "0":
                    print("Goodbye!")
                    break

                if self.current_user is None:
                    if choice == "1":
                        self.register_user()
                    elif choice == "2":
                        self.login_user()
                    else:
                        print("Invalid option.")
                else:
                    if choice == "3":
                        self.logout_user()
                    else:
                        print("Invalid option.")

            except (ValueError, RuntimeError, PermissionError) as error:
                print(f"Error: {error}")

    def register_user(self):
        username = input("Username: ")
        password = getpass("Password: ")

        user = self.auth_service.register(username, password)

        print(
            f"Account created for {user.username}. "
            f"Role: {user.role}"
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

    def logout_user(self):
        self.current_user = None
        print("You have logged out.")