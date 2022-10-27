from uuid import UUID

import pytest
from django.db import IntegrityError

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import (
    ArticleVoteEntity
)
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import (
    VotingUserEntity
)
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import (
    VotingUserNotFound
)
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import (
    VotingUserRepository
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import ArticleVote, VotingUser


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_find_voting_user_who_has_not_voted(
    voting_user_entity: VotingUserEntity,
    an_article_id: ArticleId,
    voting_user_who_has_not_voted: VotingUser
):
    voting_user_entity.save()

    voting_user = VotingUserRepository().find_voting_user(
        an_article_id,
        UserId(voting_user_entity.user_id),
    )

    assert voting_user == voting_user_who_has_not_voted


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_find_voting_user_who_has_already_voted(
    article_vote_entity: ArticleVoteEntity,
    voting_user_entity: VotingUserEntity,
    voting_user_who_has_voted: VotingUser
):
    voting_user_entity.save()
    article_vote_entity.save()

    voting_user = VotingUserRepository().find_voting_user(
        ArticleId(article_vote_entity.article_id),
        UserId(voting_user_entity.user_id)
    )

    assert voting_user == voting_user_who_has_voted


@pytest.mark.integration
@pytest.mark.django_db
def test_get_non_existing_voting_user_raises_user_not_found(a_user_id, an_article_id):
    with pytest.raises(VotingUserNotFound):
        VotingUserRepository().find_voting_user(an_article_id, a_user_id)


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_save_voting_user_with_same_vote_raises_integrity_error(voting_user: VotingUser):
    with pytest.raises(IntegrityError):
        VotingUserRepository().save_voting_user(voting_user)
        VotingUserRepository().save_voting_user(voting_user)


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_voting_user_saved(voting_user: VotingUser):
    VotingUserRepository().save_voting_user(voting_user)

    voting_user_entity = VotingUserEntity.objects.get(user_id=voting_user.id)
    assert voting_user_entity.user_id == voting_user.id
    assert voting_user_entity.karma == voting_user.karma


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_article_vote_saved(voting_user: VotingUser, article_vote: ArticleVote):
    VotingUserRepository().save_voting_user(voting_user)

    article_vote_entity = ArticleVoteEntity.objects.get(
        article_id=voting_user.votes_for_articles[0].article_id,
        user_id=voting_user.id
    )
    assert article_vote_entity.article_id == article_vote.article_id
    assert article_vote_entity.user_id == voting_user.id
    assert article_vote_entity.vote == str(article_vote.vote)


@pytest.fixture(scope='module')
def voting_user_entity() -> VotingUserEntity:
    return VotingUserEntity(
        user_id=UUID('06aee517-0000-0000-0000-000000000000'),
        karma=100
    )


@pytest.fixture(scope='module')
def article_vote_entity() -> ArticleVoteEntity:
    return ArticleVoteEntity(
        article_id=UUID('171f2557-0000-0000-0000-000000000000'),
        user_id=UUID('06aee517-0000-0000-0000-000000000000'),
        vote=ArticleVoteEntity.VOTE_UP
    )


@pytest.fixture(scope='module')
def voting_user_who_has_not_voted() -> VotingUser:
    return VotingUser(
        UserId(UUID('06aee517-0000-0000-0000-000000000000')),
        Karma(100),
        []
    )


@pytest.fixture(scope='module')
def voting_user_who_has_voted() -> VotingUser:
    return VotingUser(
        UserId(UUID('06aee517-0000-0000-0000-000000000000')),
        Karma(100),
        [
            ArticleVote(
                ArticleId(UUID('171f2557-0000-0000-0000-000000000000')),
                UserId(UUID('06aee517-0000-0000-0000-000000000000')),
                Vote.UP
            )
        ]
    )


@pytest.fixture(scope='module')
def voting_user(article_vote: ArticleVote) -> VotingUser:
    return VotingUser(
        UserId(UUID('5e3f29f9-0000-0000-0000-000000000000')),
        Karma(10),
        [article_vote]
    )


@pytest.fixture(scope='module')
def article_vote() -> ArticleVote:
    return ArticleVote(
        ArticleId(UUID('c313a2b3-0000-0000-0000-000000000000')),
        UserId(UUID('5e3f29f9-0000-0000-0000-000000000000')),
        Vote.UP
    )
