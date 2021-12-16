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
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id
from tests.test_myapp.application.domain.model.voting_user_creation import \
    (
    build_article_vote, build_voting_user
)


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
    with pytest.raises(VotingUserNotFound) as e:
        VotingUserRepository().find_voting_user(
            user_id=create_user_id(),
            article_id=uuid4()
        )


@pytest.mark.integration
@pytest.mark.django_db
def test_save_voting_user_saves_article_vote():
    voting_user = _build_voting_user_who_casted_vote_for_article(
        UserId('9317bc88-0000-0000-0000-000000000000'),
        ArticleId('40ea07ed-0000-0000-0000-000000000000'),
        Vote.UP
    )

    VotingUserRepository().save_voting_user(voting_user)

    assert ArticleVoteEntity.objects.filter(
        user_id = UUID('9317bc88-0000-0000-0000-000000000000'),
        article_id= UUID('40ea07ed-0000-0000-0000-000000000000'),
        vote=ArticleVoteEntity.VOTE_UP
    ).exists()


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
