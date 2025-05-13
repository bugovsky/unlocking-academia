import uuid
from uuid import UUID
from fastapi import HTTPException, status

import pytest

from backend.schema.user import User
from backend.service.user import UserService
from tests.factory.models import UserFactory
from tests.factory.schema import UserCreateFactory, UserUpdateFactory


@pytest.fixture
def user_service(mocked_user_repo):
    return UserService(user_repo=mocked_user_repo)

@pytest.fixture
def user_id():
    return uuid.uuid4()


class TestUserService:
    async def test_get_user_by_id_success(self, user_service, mocked_user_repo, user_id):
        user = UserFactory.build(id=user_id)
        mocked_user_repo.get_user_by_id.return_value = user

        result = await user_service.get_user_by_id(user_id)

        assert isinstance(result, User)
        assert result.id == user_id
        mocked_user_repo.get_user_by_id.assert_called_once_with(user_id)

    async def test_get_user_by_id_not_found(self, user_service, mocked_user_repo, user_id):
        mocked_user_repo.get_user_by_id.return_value = None

        with pytest.raises(HTTPException) as err:
            await user_service.get_user_by_id(user_id)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_user_repo.get_user_by_id.assert_called_once_with(user_id)

    async def test_get_not_students_success(self, user_service, mocked_user_repo):
        users = UserFactory.batch(size=2)
        mocked_user_repo.get_not_students.return_value = users

        result = await user_service.get_not_students()

        assert len(result) == 2
        assert all(isinstance(user, User) for user in result)
        mocked_user_repo.get_not_students.assert_called_once_with()

    async def test_create_user_success(self, user_service, mocked_user_repo):
        user_data = UserCreateFactory.build()
        user = UserFactory.build(email=user_data.email)
        mocked_user_repo.get_user_by_email.return_value = None
        mocked_user_repo.create_user.return_value = user

        result = await user_service.create_user(user_data)

        assert isinstance(result, User)
        assert result.email == user_data.email
        mocked_user_repo.get_user_by_email.assert_called_once_with(email=user_data.email)
        mocked_user_repo.create_user.assert_called_once_with(user_data)

    async def test_create_user_already_exists(self, user_service, mocked_user_repo):
        user_data = UserCreateFactory.build()
        mocked_user_repo.get_user_by_email.return_value = object()

        with pytest.raises(HTTPException) as err:
            await user_service.create_user(user_data)

        assert err.value.status_code == status.HTTP_409_CONFLICT
        mocked_user_repo.get_user_by_email.assert_called_once_with(email=user_data.email)

    async def test_update_user_success(self, user_service, mocked_user_repo, user_id):
        user_data = UserUpdateFactory.build()
        user = UserFactory.build(id=user_id)
        mocked_user_repo.update_user.return_value = user

        result = await user_service.update_user(user_id, user_data)

        assert isinstance(result, User)
        assert result.id == user_id
        mocked_user_repo.update_user.assert_called_once_with(user_id, user_data)

    async def test_update_user_not_found(self, user_service, mocked_user_repo, user_id):
        user_data = UserUpdateFactory.build()
        mocked_user_repo.update_user.return_value = None

        with pytest.raises(HTTPException) as err:
            await user_service.update_user(user_id, user_data)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_user_repo.update_user.assert_called_once_with(user_id, user_data)