import pytest

from chatnews.core.entities.models.user import User
from chatnews.pipelines.steps import get_or_create_user


@pytest.fixture(scope="module")
def user() -> User:
    user: User = User(first_name="bob", last_name="bob")
    return user


def test_get_metadata(user: User) -> None:
    user_full_name = "bob bob"
    assert get_or_create_user._get_metadata(user_full_name, user) == {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }


def test_get_or_create_user(user: User) -> None:
    user_get = get_or_create_user._get_or_create_user(user.full_name)
    assert user_get.first_name == user.first_name
    assert user_get.last_name == user.last_name
