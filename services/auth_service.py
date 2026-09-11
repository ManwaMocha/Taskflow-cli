"""Registration and login logic."""

import bcrypt

from models.user import Admin, Member, User

#performs authentication operations
class AuthService:
    def __init__(self, user_storage):
        self.user_storage = user_storage
    def register(self, username, password):
        username = username.strip()

        if len(username) < 3:
            raise ValueError("Username must contain at least 3 characters.")

        if len(password) < 6:
            raise ValueError("Password must contain at least 6 characters.")

        users = self.user_storage.load()
#checks whether at least one saved username matches
        if any(
            user["username"].lower() == username.lower()
            for user in users
        ):
            raise ValueError("That username already exists.")