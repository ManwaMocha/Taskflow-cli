"Comment business logic."

from models.comment import Comment


class CommentService:
    def __init__(self, comment_storage):
        # receiving the storage object used to save comments.
        self.comment_storage = comment_storage

    def create(self, task_id, user_id, message):
        # creating a new Comment with the next available ID.
        comment = Comment(
            self.comment_storage.next_id(),
            task_id,
            user_id,
            message
        )

        # converting the Comment to a dictionary and saving it.
        self.comment_storage.add(comment.to_dict())

        # returning the created Comment object.
        return comment

    def list_for_task(self, task_id):
        # loading all comments and keeping only those for this task.
        return [
            Comment.from_dict(item)
            for item in self.comment_storage.load()
            if item["task_id"] == task_id
        ]
