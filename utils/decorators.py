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