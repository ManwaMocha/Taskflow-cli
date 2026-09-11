class User:
    VALID_ROLES = {"admin", "member"}

    def __init__(self, user_id, username, password_hash, role="member"):
        if role not in self.VALID_ROLES:
            raise ValueError("Role must be admin or member.")

        self.id = user_id
        self.username = username
        self.__password_hash = password_hash
        self.role = role

    @property #cant replace the password
    def password_hash(self):
        """Provide read-only access to the private password hash."""
        return self.__password_hash

    def can_manage_users(self):
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.__password_hash,
            "role": self.role,
        }

class Admin(User):
    def __init__(self, user_id, username, password_hash):
        super().__init__(
            user_id,
            username,
            password_hash,
            "admin",
        )#calls the parent User

    def can_manage_users(self):
        return True #polymorphism


class Member(User):
    def __init__(self, user_id, username, password_hash):
        super().__init__(
            user_id,
            username,
            password_hash,
            "member",
        )