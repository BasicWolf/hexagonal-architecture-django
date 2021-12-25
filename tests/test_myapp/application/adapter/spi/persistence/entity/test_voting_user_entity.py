from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser


def test_voting_user_entity_to_domain_model():
    entity = VotingUserEntity(
        user_id=UUID('bd9fd128-0000-0000-0000-000000000000'),
        karma=15
    )

    voting_user = entity.to_domain_model(None)

    assert voting_user == VotingUser(
        UserId(UUID('bd9fd128-0000-0000-0000-000000000000')),
        Karma(15)
    )


def test_voting_user_with_article_vote_to_domain_model():
    entity = VotingUserEntity(
        user_id=UUID('4a554f51-0000-0000-0000-000000000000'),
        karma=22
    )

    voting_user = entity.to_domain_model(
        ArticleVote(
            ArticleId(UUID('f8ca014b-0000-0000-0000-000000000000')),
            UserId(UUID('4a554f51-0000-0000-0000-000000000000')),
            Vote.DOWN
        )
    )

    assert voting_user == VotingUser(
        UserId(UUID('4a554f51-0000-0000-0000-000000000000')),
        Karma(22),
        ArticleVote(
            ArticleId(UUID('f8ca014b-0000-0000-0000-000000000000')),
            UserId(UUID('4a554f51-0000-0000-0000-000000000000')),
            Vote.DOWN
        )
    )
