from uuid import UUID

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


@pytest.mark.integration
@pytest.mark.django_db
def test_find_voting_user_who_has_not_voted(article_id: ArticleId):
    VotingUserEntity(
        user_id=UUID('06aee517-0000-0000-0000-000000000000'),
        karma=100
    ).save()

    ArticleVoteEntity(
        article_id=UUID('171f2557-0000-0000-0000-000000000000'),
        user_id=UUID('06aee517-0000-0000-0000-000000000000'),
    ).save()

    voting_user = VotingUserRepository().find_voting_user(
        ArticleId(UUID('171f2557-0000-0000-0000-000000000000')),
        UserId(UUID('06aee517-0000-0000-0000-000000000000'))
    )

    assert voting_user.id == UserId(UUID('06aee517-0000-0000-0000-000000000000'))
    assert voting_user.karma == Karma(100)
    assert voting_user.voted_for_articles == [
        ArticleId(UUID('171f2557-0000-0000-0000-000000000000'))
    ]


@pytest.mark.integration
@pytest.mark.django_db
def test_find_voting_user_who_has_already_voted():
    VotingUserEntity(
        user_id=UUID('34d00b01-0000-0000-0000-000000000000'),
        karma=123
    ).save()

    ArticleVoteEntity(
        article_id=UUID('f784e16f-0000-0000-0000-000000000000'),
        user_id=UUID('34d00b01-0000-0000-0000-000000000000'),
        vote=ArticleVoteEntity.VOTE_UP
    ).save()

    voting_user = VotingUserRepository().find_voting_user(
        ArticleId(UUID('f784e16f-0000-0000-0000-000000000000')),
        UserId(UUID('34d00b01-0000-0000-0000-000000000000'))
    )

    assert ArticleId(UUID('f784e16f-0000-0000-0000-000000000000')) in voting_user.voted_for_articles  # noqa


@pytest.mark.integration
@pytest.mark.django_db
def test_get_non_existing_voting_user_raises_user_not_found(user_id, article_id):
    with pytest.raises(VotingUserNotFound):
        VotingUserRepository().find_voting_user(article_id, user_id)
