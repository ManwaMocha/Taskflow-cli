"""Decorators for authentication, authorization, and logging."""

from functools import wraps
import logging


def login_required(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            raise PermissionError("You must log in first.")

        return function(self, *args, **kwargs)

    return wrapper
def role_required(required_role):
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if self.current_user is None:
                raise PermissionError("You must log in first.")

            if self.current_user.role != required_role:
                raise PermissionError(
                    f"Only {required_role}s can perform this action."
                )

            return function(self, *args, **kwargs)

        return wrapper

    return decorator