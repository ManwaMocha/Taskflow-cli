"""Registration and login logic."""

import bcrypt

from models.user import Admin, Member, User

#performs authentication operations amd rules
class AuthService:
    def __init__(self, user_storage):
        self.user_storage = user_storage#user json details
    def register(self, username, password):
        username = username.strip()

        if len(username) < 3:
            raise ValueError("Username must contain at least 3 characters.")

        if len(password) < 6:
            raise ValueError("Password must contain at least 6 characters.")

        users = self.user_storage.load()#load existing users
#checks whether at least one saved username matches
        if any(
            user["username"].lower() == username.lower()
            for user in users
        ):
            raise ValueError("That username already exists.")
        password_hash = bcrypt.hashpw(
            password.encode(),#python string to bytes
            bcrypt.gensalt(),#creates salt which make identical passwords produce different hashes
        ).decode()#converts the bytes back into a string so it can be saved on json

        user_id = self.user_storage.next_id()

        if not users:
            user = Admin(user_id, username, password_hash)
        else:
            user = Member(user_id, username, password_hash)

        self.user_storage.add(user.to_dict())

        return user
    def login(self, username, password):
        #loop through users and return user if its username matches
        record = next(#function that takes the next available value from an iterator
            (
                user
                for user in self.user_storage.load()
                if user["username"].lower() == username.strip().lower()
            ),
            None,
        )

        if record is None:
            return None

        if not bcrypt.checkpw(
            password.encode(),
            record["password_hash"].encode(),
        ):
            return None

        return User.from_dict(record)#converts the dictionary into an Admin or member object