from decimal import Decimal
import uuid
from fastapi import HTTPException, status

import pytest

from backend.schema.rating import RatingByUser, PostRating
from backend.service.rating import RatingService
from tests.factory.models import RatingFactory
from tests.factory.schema import RatingCreateFactory, RatingUpdateFactory

@pytest.fixture
def rating_service(mocked_rating_repo):
    return RatingService(rating_repo=mocked_rating_repo)

@pytest.fixture
def post_id():
    return uuid.uuid4()

@pytest.fixture
def user_id():
    return uuid.uuid4()

class TestRatingService:
    async def test_get_post_rating_success(self, rating_service, mocked_rating_repo, post_id):
        mocked_rating_repo.get_post_rating.return_value = Decimal("8.5")

        result = await rating_service.get_post_rating(post_id)

        assert isinstance(result, PostRating)
        assert result.grade == Decimal("8.50")
        assert result.post_id == post_id
        mocked_rating_repo.get_post_rating.assert_called_once_with(post_id)

    async def test_get_post_rating_none(self, rating_service, mocked_rating_repo, post_id):
        mocked_rating_repo.get_post_rating.return_value = None

        result = await rating_service.get_post_rating(post_id)

        assert result is None
        mocked_rating_repo.get_post_rating.assert_called_once_with(post_id)

    async def test_rate_success(self, rating_service, mocked_rating_repo, post_id, user_id):
        rating_data = RatingCreateFactory.build()
        rating = RatingFactory.build(post_id=post_id)
        mocked_rating_repo.get_rating_by_user.return_value = None
        mocked_rating_repo.rate.return_value = rating

        result = await rating_service.rate(post_id, user_id, rating_data)

        assert isinstance(result, RatingByUser)
        assert result.post_id == post_id
        mocked_rating_repo.get_rating_by_user.assert_called_once_with(post_id=post_id, user_id=user_id)
        mocked_rating_repo.rate.assert_called_once_with(post_id, user_id, rating_data)

    async def test_rate_already_rated(self, rating_service, mocked_rating_repo, post_id, user_id):
        rating_data = RatingCreateFactory.build()
        mocked_rating_repo.get_rating_by_user.return_value = object()

        with pytest.raises(HTTPException) as err:
            await rating_service.rate(post_id, user_id, rating_data)

        assert err.value.status_code == status.HTTP_409_CONFLICT
        mocked_rating_repo.get_rating_by_user.assert_called_once_with(post_id=post_id, user_id=user_id)

    async def test_update_rating_success(self, rating_service, mocked_rating_repo, post_id, user_id):
        rating_data = RatingUpdateFactory.build()
        rating = RatingFactory.build(post_id=post_id)
        mocked_rating_repo.get_rating_by_user.return_value = object()
        mocked_rating_repo.update_rating.return_value = rating

        result = await rating_service.update_rating(post_id, user_id, rating_data)

        assert isinstance(result, RatingByUser)
        assert result.post_id == post_id
        mocked_rating_repo.get_rating_by_user.assert_called_once_with(post_id=post_id, user_id=user_id)
        mocked_rating_repo.update_rating.assert_called_once_with(post_id, user_id, rating_data)

    async def test_update_rating_not_rated(self, rating_service, mocked_rating_repo, post_id, user_id):
        rating_data = RatingUpdateFactory.build()
        mocked_rating_repo.get_rating_by_user.return_value = None

        with pytest.raises(HTTPException) as err:
            await rating_service.update_rating(post_id, user_id, rating_data)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_rating_repo.get_rating_by_user.assert_called_once_with(post_id=post_id, user_id=user_id)