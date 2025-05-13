import uuid

import pytest
from fastapi import status

from backend.schema.request import Request
from backend.schema.user import Role
from tests.factory.schema import RequestFactory, RequestCreateFactory, RequestCloseFactory, UserFactory


@pytest.fixture(scope="class")
def request_id():
    return uuid.uuid4()


class TestRequest:
    def test_create_request_success(self, backend_client, mocked_request_service, mocked_user_service):
        user = UserFactory.build(role=Role.STUDENT)
        request_data = RequestCreateFactory.build()
        expected_request = RequestFactory.build(author_id=user.id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_request_service.create_request.return_value = expected_request


        response = backend_client.post(
            "/request",
            params={"user_id": user.id, "role": user.role},
            json=request_data.model_dump(mode="json")
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Request.model_validate(response.json()) == expected_request
        mocked_request_service.create_request.assert_called_once_with(
            user_id=user.id, request_data=request_data
        )

    def test_get_request_success(self, backend_client, mocked_request_service, mocked_user_service, request_id):
        user = UserFactory.build(role=Role.STUDENT)
        expected_request = RequestFactory.build(author_id=user.id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_request_service.get_request_by_id.return_value = expected_request

        response = backend_client.get(
            f"/request/{request_id}",
            params={"user_id": user.id, "role": user.role}
        )

        assert response.status_code == status.HTTP_200_OK
        assert Request.model_validate(response.json()) == expected_request
        mocked_request_service.get_request_by_id.assert_called_once_with(
            user_id=user.id, request_id=request_id
        )

    def test_get_user_requests_success(self, backend_client, mocked_request_service, mocked_user_service):
        user = UserFactory.build(role=Role.STUDENT)
        expected_requests = RequestFactory.batch(size=2, author_id=user.id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_request_service.get_user_requests.return_value = expected_requests

        response = backend_client.get(
            "/request",
            params={"user_id": user.id, "role": user.role}
        )

        assert response.status_code == status.HTTP_200_OK
        assert [Request.model_validate(item) for item in response.json()] == expected_requests
        mocked_request_service.get_user_requests.assert_called_once_with(user_id=user.id)

    def test_close_request_success(self, backend_client, mocked_request_service, mocked_user_service, request_id):
        user = UserFactory.build(role=Role.STUDENT)
        request_data = RequestCloseFactory.build()
        expected_request = RequestFactory.build(recipient_id=user.id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_request_service.close_request.return_value = expected_request

        response = backend_client.patch(
            f"/request/{request_id}",
            params={"user_id": user.id, "role": user.role},
            json=request_data.model_dump()
        )

        assert response.status_code == status.HTTP_200_OK
        assert Request.model_validate(response.json()) == expected_request
        mocked_request_service.close_request.assert_called_once_with(
            user_id=user.id, request_id=request_id, request_data=request_data
        )