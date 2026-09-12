from models.project import Project

class ProjectService:
    def __init__(self, project_storage):
        self.project_storage = project_storage

    def create(self, name, description, created_by):
        project = Project(
            self.project_storage.next_id(),
            name,
            description,
            created_by,
            member_ids=[created_by]
        )
        self.project_storage.add(project.to_dict())
        return project

    def list_all(self):
        return [Project.from_dict(item) for item in self.project_storage.load()]

    def get(self, project_id):
        record = self.project_storage.find_by_id(project_id)
        return Project.from_dict(record) if record else None





