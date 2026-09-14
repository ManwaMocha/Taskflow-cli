import logging

import pytest

from models.user import Admin, Member
from utils.decorators import (
    log_action,
    login_required,
    role_required,
)


class FakeApp:
    def __init__(self, current_user=None):
        self.current_user = current_user

    @login_required
    def protected_action(self):
        return "Action allowed"

    @role_required("admin")
    def admin_action(self):
        return "Admin action allowed"

    @log_action
    def logged_action(self):
        return "Logged action completed"


def test_login_required_blocks_logged_out_user():
    app = FakeApp()

    with pytest.raises(PermissionError):
        app.protected_action()


def test_login_required_allows_logged_in_user():
    app = FakeApp(current_user=object())

    result = app.protected_action()

    assert result == "Action allowed"


def test_role_required_blocks_logged_out_user():
    app = FakeApp()

    with pytest.raises(PermissionError):
        app.admin_action()


def test_role_required_blocks_member():
    member = Member(2, "member", "test_hash")
    app = FakeApp(current_user=member)

    with pytest.raises(PermissionError):
        app.admin_action()


def test_role_required_allows_admin():
    admin = Admin(1, "leader", "test_hash")
    app = FakeApp(current_user=admin)

    result = app.admin_action()

    assert result == "Admin action allowed"


def test_log_action_records_success(caplog):
    app = FakeApp()

    with caplog.at_level(logging.INFO):
        result = app.logged_action()

    assert result == "Logged action completed"
    assert "Action completed: logged_action" in caplog.text