import uuid

import pytest
from fastapi import status

from backend.schema.rating import RatingByUser, PostRating
from backend.schema.user import Role
from tests.factory.schema import RatingCreateFactory, RatingByUserFactory, PostRatingFactory, RatingUpdateFactory, UserFactory


@pytest.fixture(scope="class")
def post_id():
    return uuid.uuid4()


class TestRating:
    def test_rate_post_success(self, backend_client, mocked_rating_service, mocked_user_service, post_id):
        user = UserFactory.build(role=Role.STUDENT)
        rating_data = RatingCreateFactory.build()
        expected_rating = RatingByUserFactory.build(post_id=post_id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_rating_service.rate.return_value = expected_rating

        response = backend_client.post(
            f"/rating/{post_id}",
            params={"user_id": user.id, "role": user.role},
            json=rating_data.model_dump()
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert RatingByUser.model_validate(response.json()) == expected_rating
        mocked_rating_service.rate.assert_called_once_with(
            post_id=post_id, user_id=user.id, rating_data=rating_data
        )

    def test_get_post_rating_success(self, backend_client, mocked_rating_service, post_id):
        expected_rating = PostRatingFactory.build(post_id=post_id)
        mocked_rating_service.get_post_rating.return_value = expected_rating

        response = backend_client.get(f"/rating/{post_id}")

        assert response.status_code == status.HTTP_200_OK
        assert PostRating.model_validate(response.json()) == expected_rating
        mocked_rating_service.get_post_rating.assert_called_once_with(post_id)

    def test_get_post_rating_none(self, backend_client, mocked_rating_service, post_id):
        mocked_rating_service.get_post_rating.return_value = None

        response = backend_client.get(f"/rating/{post_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None
        mocked_rating_service.get_post_rating.assert_called_once_with(post_id)

    def test_update_post_rating_success(self, backend_client, mocked_rating_service, mocked_user_service, post_id):
        user = UserFactory.build(role=Role.STUDENT)
        rating_update = RatingUpdateFactory.build()
        expected_rating = RatingByUserFactory.build(post_id=post_id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_rating_service.update_rating.return_value = expected_rating

        response = backend_client.patch(
            f"/rating/{post_id}",
            params={"user_id": user.id, "role": user.role},
            json=rating_update.model_dump()
        )

        assert response.status_code == status.HTTP_200_OK
        assert RatingByUser.model_validate(response.json()) == expected_rating
        mocked_rating_service.update_rating.assert_called_once_with(
            post_id=post_id, user_id=user.id, rating_data=rating_update
        )