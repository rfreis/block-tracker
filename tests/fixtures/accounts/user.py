import pytest

from tests.fixtures.utils import delete_related_obj

from accounts.models import User


@pytest.fixture
def default_password():
    return "default_pass"


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_one(default_password):
    user = User.objects.create(
        first_name="User",
        last_name="One",
        username="user_one@email.com",
        email="user_one@email.com",
    )
    user.set_password(default_password)
    user.save()

    yield user

    delete_related_obj(user)


@pytest.fixture
@pytest.mark.usefixtures("db")
def user_two(default_password):
    user = User.objects.create(
        first_name="User",
        last_name="Two",
        username="user_two@email.com",
        email="user_two@email.com",
    )
    user.set_password(default_password)
    user.save()

    yield user

    delete_related_obj(user)


@pytest.fixture
def client_user_one(user_one, client):
    client.force_login(user_one)
    yield client
