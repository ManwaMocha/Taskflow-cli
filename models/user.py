"""User models demonstrate inheritance and encapsulation."""


class User:
    VALID_ROLES = {"admin", "member"}

    def __init__(self, user_id, username, password_hash, role="member"):
        if role not in self.VALID_ROLES:
            raise ValueError("Role must be admin or member.")

        self.id = user_id
        self.username = username
        self.__password_hash = password_hash
        self.role = role
        