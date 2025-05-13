import uuid

import pytest
from fastapi import status

from backend.schema.user import User
from tests.factory.schema import UserFactory, UserCreateFactory, UserUpdateFactory


@pytest.fixture(scope="class")
def user_id():
    return uuid.uuid4()


class TestUser:
    def test_create_user_success(self, backend_client, mocked_user_service):
        user_data = UserCreateFactory.build()
        expected_user = UserFactory.build(email=user_data.email)
        mocked_user_service.create_user.return_value = expected_user

        payload = {**user_data.model_dump(exclude={"password"}), "password": user_data.password.get_secret_value()}
        response = backend_client.post("/user", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.model_validate(response.json()) == expected_user
        mocked_user_service.create_user.assert_called_once_with(user_data=user_data)

    def test_get_experts_success(self, backend_client, mocked_user_service):
        expected_users = UserFactory.batch(size=2)
        mocked_user_service.get_not_students.return_value = expected_users

        response = backend_client.get("/user/experts")

        assert response.status_code == status.HTTP_200_OK
        assert [User.model_validate(item) for item in response.json()] == expected_users
        mocked_user_service.get_not_students.assert_called_once_with()

    def test_get_user_by_id_success(self, backend_client, mocked_user_service, user_id):
        expected_user = UserFactory.build(id=user_id)
        mocked_user_service.get_user_by_id.return_value = expected_user

        response = backend_client.get(
            f"/user/{user_id}",
            params={"user_id": user_id, "role": expected_user.role}
        )

        assert response.status_code == status.HTTP_200_OK
        assert User.model_validate(response.json()) == expected_user
        mocked_user_service.get_user_by_id.assert_called_once_with(user_id=user_id)

    def test_update_user_success(self, backend_client, mocked_user_service, user_id):
        user = UserFactory.build(id=user_id)
        user_data = UserUpdateFactory.build()
        expected_user = UserFactory.build(id=user_id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_user_service.update_user.return_value = expected_user

        response = backend_client.patch(
            f"/user/{user_id}",
            params={"user_id": user_id, "role": user.role},
            json=user_data.model_dump()
        )

        assert response.status_code == status.HTTP_200_OK
        assert User.model_validate(response.json()) == expected_user
        mocked_user_service.update_user.assert_called_once_with(user_id, user_data)