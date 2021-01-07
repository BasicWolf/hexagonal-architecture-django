import pytest

from myapp.application.adapter.spi.persistence.entity.vote_casting_user_entity import \
    VoteCastingUserEntity
from myapp.application.adapter.spi.persistence.repository.vote_casting_user_repository import \
    VoteCastingUserRepository


@pytest.mark.django_db
def test_get_vote_casting_user(user_id):
    vote_casting_repository = VoteCastingUserRepository()

    VoteCastingUserEntity(
        user_id=user_id,
        karma=100
    ).save()

    vote_casting_user = vote_casting_repository.get_vote_casting_user(
        user_id=user_id
    )

    assert vote_casting_user.id == user_id
    assert vote_casting_user.karma == 100


