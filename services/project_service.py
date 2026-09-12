from models.project import Project

class ProjectService:
    def __init__(self, project_storage):
        self.project_storage = project_storage

    def create(self, name, description, created_by):
        project = Project(
            self.project_storage.next_id(),
        )




