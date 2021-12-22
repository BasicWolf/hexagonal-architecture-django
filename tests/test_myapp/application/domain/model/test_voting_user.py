from uuid import UUID

import pytest

from myapp.application.domain.model.cast_article_vote_result import (
    InsufficientKarma,
    VoteAlreadyCast, VoteSuccessfullyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from tests.test_myapp.application.domain.model.builder.article_vote_creation import \
    build_article_vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import \
    (
    build_voting_user
)
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id


@pytest.mark.parametrize('cast_vote,result_vote', [
    (Vote.UP, Vote.UP),
    (Vote.DOWN, Vote.DOWN)
])
def test_cast_vote_updates_user_vote(
    cast_vote: Vote,
    result_vote: Vote,
):
    voting_user = build_voting_user()
    voting_user.cast_vote(create_article_id(), cast_vote)

    assert voting_user.article_vote.vote == result_vote


def test_cast_vote_returns_vote_cast(
    user_id: UserId,
    article_id: ArticleId
):
    voting_user = build_voting_user(
        user_id=user_id,
        karma=Karma(5)
    )

    result = voting_user.cast_vote(article_id, Vote.UP)

    assert isinstance(result, VoteSuccessfullyCast)
    assert result.vote == Vote.UP
    assert result.article_id == article_id
    assert result.user_id == user_id


def test_cannot_cast_vote_with_insufficient_karma(user_id: UserId, article_id: ArticleId):
    voting_user = build_voting_user(
        user_id=user_id,
        karma=Karma(4)
    )

    result = voting_user.cast_vote(article_id, Vote.UP)

    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_casting_vote_returns_already_cast():
    voting_user = build_voting_user(
        user_id=UserId(UUID('476820aa-0000-0000-0000-000000000000')),
        article_vote=build_article_vote(
            UserId(UUID('476820aa-0000-0000-0000-000000000000')),
            ArticleId(UUID('d07af0ab-0000-0000-0000-000000000000')),
        )
    )

    result = voting_user.cast_vote(
        ArticleId(UUID('d07af0ab-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert isinstance(result, VoteAlreadyCast)
    assert result.user_id == UserId(UUID('476820aa-0000-0000-0000-000000000000'))
    assert result.article_id == ArticleId(UUID('d07af0ab-0000-0000-0000-000000000000'))


def test_cannot_cast_vote_twice():
    voting_user = build_voting_user(
        user_id=UserId(UUID('9ab9ac19-0000-0000-0000-000000000000')),
        article_vote=build_article_vote(
            article_id=ArticleId(UUID('01ec495e-0000-0000-0000-000000000000')),
            vote=Vote.UP
        )
    )

    result = voting_user.cast_vote(
        ArticleId(UUID('01ec495e-0000-0000-0000-000000000000')),
        Vote.UP
    )

    assert isinstance(result, VoteAlreadyCast)
