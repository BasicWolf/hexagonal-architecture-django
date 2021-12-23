from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


def test_voting_user_entity_to_domain_model():
    entity = VotingUserEntity(
        user_id=UUID('bd9fd128-0000-0000-0000-000000000000'),
        karma=15
    )

    voting_user = entity.to_domain_model()

    assert voting_user == VotingUser(
        UserId(UUID('bd9fd128-0000-0000-0000-000000000000')),
        Karma(15)
    )
