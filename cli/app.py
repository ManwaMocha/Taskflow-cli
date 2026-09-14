"""Interactive command-line interface."""


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