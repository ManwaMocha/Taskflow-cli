import bcrypt
import pytest

from services.auth_service import AuthService

class FakeStorage:
    def __init__(self):
        self.records = []

    def load(self):
        return self.records

    def next_id(self):
        return len(self.records) + 1

    def add(self, record):
        self.records.append(record)
        return record

    def find_by_id(self, record_id):
        for record in self.records:
            if record["id"] == record_id:
                return record

        return None
def test_first_registered_user_is_admin():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    user = auth_service.register("leader", "secret1")

    assert user.role == "admin"
    assert user.can_manage_users() is True
    assert len(storage.records) == 1
def test_second_registered_user_is_member():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    auth_service.register("leader", "secret1")
    member = auth_service.register("member", "secret2")

    assert member.role == "member"
    assert member.can_manage_users() is False
    assert len(storage.records) == 2

def test_password_is_hashed():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    auth_service.register("leader", "secret1")

    saved_user = storage.records[0]
    saved_hash = saved_user["password_hash"]

    assert saved_hash != "secret1"
    assert bcrypt.checkpw(
        "secret1".encode(),
        saved_hash.encode(),
    )
def test_login_with_correct_password():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    auth_service.register("leader", "secret1")

    logged_in_user = auth_service.login("leader", "secret1")

    assert logged_in_user is not None
    assert logged_in_user.username == "leader"
    assert logged_in_user.role == "admin"


def test_login_with_wrong_password():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    auth_service.register("leader", "secret1")

    logged_in_user = auth_service.login("leader", "wrongpassword")

    assert logged_in_user is None

def test_duplicate_username_is_rejected():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    auth_service.register("leader", "secret1")

    with pytest.raises(ValueError):
        auth_service.register("LEADER", "secret2")

def test_list_and_get_users():
    storage = FakeStorage()
    auth_service = AuthService(storage)

    leader = auth_service.register("leader", "secret1")
    member = auth_service.register("member", "secret2")

    users = auth_service.list_users()

    assert len(users) == 2
    assert users[0].username == "leader"
    assert users[1].username == "member"

    found_user = auth_service.get_user(member.id)

    assert found_user is not None
    assert found_user.id == member.id
    assert found_user.username == "member"

    missing_user = auth_service.get_user(999)

    assert missing_user is None
def test_login_required_blocks_logged_out_user():
    app = FakeApp()

    with pytest.raises(PermissionError):
        app.protected_action()


def test_login_required_allows_logged_in_user():
    app = FakeApp(current_user=object())

    result = app.protected_action()

    assert result == "Action allowed"