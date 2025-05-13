import uuid
from fastapi import HTTPException, status

import pytest

from backend.schema.request import Request
from backend.service.request import RequestService
from tests.factory.models import RequestFactory, UserFactory
from tests.factory.schema import RequestCreateFactory, RequestCloseFactory


@pytest.fixture
def request_service(mocked_request_repo, mocked_user_repo):
    return RequestService(request_repo=mocked_request_repo, user_repo=mocked_user_repo)

@pytest.fixture
def request_id():
    return uuid.uuid4()

@pytest.fixture
def user_id():
    return uuid.uuid4()


class TestRequestService:
    async def test_get_request_by_id_success(
        self, request_service, mocked_request_repo, mocked_user_repo, request_id, user_id
    ):
        request = RequestFactory.build(id=request_id, author_id=user_id)
        mocked_request_repo.get_request_by_id.return_value = request

        result = await request_service.get_request_by_id(user_id, request_id)

        assert isinstance(result, Request)
        assert result.id == request_id
        mocked_request_repo.get_request_by_id.assert_called_once_with(request_id)

    async def test_get_request_by_id_not_found(
        self, request_service, mocked_request_repo, mocked_user_repo, request_id, user_id
    ):
        mocked_request_repo.get_request_by_id.return_value = None

        with pytest.raises(HTTPException) as err:
            await request_service.get_request_by_id(user_id, request_id)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_request_repo.get_request_by_id.assert_called_once_with(request_id)

    async def test_get_request_by_id_forbidden(
        self, request_service, mocked_request_repo, mocked_user_repo, request_id, user_id
    ):
        request = RequestFactory.build(author_id=uuid.uuid4())
        mocked_request_repo.get_request_by_id.return_value = request

        with pytest.raises(HTTPException) as err:
            await request_service.get_request_by_id(user_id, request_id)

        assert err.value.status_code == status.HTTP_403_FORBIDDEN
        mocked_request_repo.get_request_by_id.assert_called_once_with(request_id)

    async def test_get_user_requests_success(
        self, request_service, mocked_request_repo, mocked_user_repo, user_id
    ):
        requests = RequestFactory.batch(size=2, author_id=user_id)
        mocked_request_repo.get_user_requests.return_value = requests

        result = await request_service.get_user_requests(user_id)

        assert len(result) == 2
        assert all(isinstance(request, Request) for request in result)
        mocked_request_repo.get_user_requests.assert_called_once_with(user_id)

    async def test_close_request_success(
        self, request_service, mocked_request_repo, mocked_user_repo, request_id, user_id
    ):
        request_data = RequestCloseFactory.build()
        request = RequestFactory.build(id=request_id, recipient_id=user_id)
        mocked_request_repo.get_request_by_id.return_value = request
        mocked_request_repo.close_request.return_value = request

        result = await request_service.close_request(user_id, request_id, request_data)

        assert isinstance(result, Request)
        assert result.id == request_id
        mocked_request_repo.get_request_by_id.assert_called_once_with(request_id)
        mocked_request_repo.close_request.assert_called_once_with(request_id, request_data)