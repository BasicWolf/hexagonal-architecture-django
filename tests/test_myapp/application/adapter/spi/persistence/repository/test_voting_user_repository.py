import pytest

from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


@pytest.mark.integration
@pytest.mark.django_db
def test_find_voting_user(user_id: UserId):
    VotingUserEntity(
        user_id=user_id,
        karma=100
    ).save()

    voting_user = VotingUserRepository().find_voting_user(
        user_id=user_id
    )

    assert voting_user.id == user_id
    assert voting_user.karma == Karma(100)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_non_existing_voting_user_raises_user_not_found():
    with pytest.raises(VotingUserNotFound):
        VotingUserRepository().find_voting_user(
            user_id=create_user_id()
        )
