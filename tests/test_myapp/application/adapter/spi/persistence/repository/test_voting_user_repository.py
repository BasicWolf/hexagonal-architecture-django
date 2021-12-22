import pytest

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.builder.article_vote_creation import \
    build_article_vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


@pytest.mark.integration
@pytest.mark.django_db
def test_find_voting_user(user_id: UserId, article_id: ArticleId):
    ArticleVoteEntity(
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_UP
    ).save()

    VotingUserEntity(
        user_id=user_id,
        karma=100
    ).save()

    voting_user = VotingUserRepository().find_voting_user(
        user_id=user_id,
        article_id=article_id
    )

    assert voting_user.id == user_id
    assert voting_user.voted
    assert voting_user.karma == Karma(100)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_non_existing_voting_user_raises_user_not_found():
    with pytest.raises(VotingUserNotFound):
        VotingUserRepository().find_voting_user(
            user_id=create_user_id(),
            article_id=create_article_id()
        )


def _build_voting_user_who_casted_vote_for_article(
    user_id: UserId,
    article_id: ArticleId,
    vote: Vote
) -> VotingUser:
    return build_voting_user(
        user_id=user_id,
        article_vote=build_article_vote(
            article_id=article_id,
            vote=vote
        )
    )
