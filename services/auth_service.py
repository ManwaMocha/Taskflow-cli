"""Registration and login logic."""

import bcrypt

from models.user import Admin, Member, User

#performs authentication operations
class AuthService:
    def __init__(self, user_storage):
        self.user_storage = user_storage