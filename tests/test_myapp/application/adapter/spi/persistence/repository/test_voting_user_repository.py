from uuid import UUID, uuid4

import pytest

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.domain.model.identifier.user_id import UserId
from tests.test_myapp.application.domain.model.voting_user import createUserId


@pytest.mark.integration
@pytest.mark.django_db
def test_find_voting_user(user_id: UserId, article_id: UUID):
    ArticleVoteEntity(
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_UP
    ).save()

    VotingUserEntity(
        id=user_id,
        karma=100
    ).save()

    voting_user = VotingUserRepository().find_voting_user(
        user_id=user_id,
        article_id=article_id
    )

    assert voting_user.id == user_id
    assert voting_user.voting_for_article_id == article_id
    assert voting_user.voted
    assert voting_user.karma == 100


@pytest.mark.integration
@pytest.mark.django_db
def test_get_non_existing_voting_user_raises_user_not_found():
    with pytest.raises(VotingUserNotFound) as e:
        VotingUserRepository().find_voting_user(
            user_id=createUserId(),
            article_id=uuid4()
        )

