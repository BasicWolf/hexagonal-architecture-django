from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


def test_create_voting_user_entity():
    entity = VotingUserEntity.create(
        user_id=UUID('ddb17f7a-0000-0000-0000-000000000000'),
        karma=25,
        voted=True
    )
    assert entity.user_id == UUID('ddb17f7a-0000-0000-0000-000000000000')
    assert entity.karma == 25
    assert entity.voted


def test_voting_user_entity_to_domain_model():
    entity = VotingUserEntity.create(
        user_id=UUID('bd9fd128-0000-0000-0000-000000000000'),
        karma=15,
        voted=True
    )

    voting_user = entity.to_domain_model()

    assert voting_user == VotingUser(
        UserId(UUID('bd9fd128-0000-0000-0000-000000000000')),
        Karma(15),
        voted=True
    )
