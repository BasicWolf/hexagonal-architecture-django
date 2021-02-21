from uuid import uuid4

import pytest

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser, \
    InsufficientKarma, VoteAlreadyCast
from tests.test_myapp.application.domain.model.voting_user import build_voting_user


@pytest.mark.parametrize(
    'karma', [5, 10]
)
def test_cast_vote_returns_article_vote(user_id, article_id, karma):
    voting_user = build_voting_user(
        user_id=user_id,
        karma=10
    )

    result = voting_user.cast_vote(
        article_id=article_id,
        vote=Vote.UP
    )

    assert isinstance(result, ArticleVote)
    assert result.vote == Vote.UP
    assert result.article_id == article_id
    assert result.user_id == user_id


def test_cannot_cast_vote_with_insufficient_karma(user_id):
    voting_user = build_voting_user(
        user_id=user_id,
        karma=4
    )

    result = voting_user.cast_vote(
        article_id=uuid4(),
        vote=Vote.UP
    )

    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_cannot_cast_vote_twice(user_id, article_id):
    voting_user = VotingUser(
        id=user_id,
        voting_for_article_id=article_id,
        voted=True,
        karma=10
    )

    result = voting_user.cast_vote(
        article_id=article_id,
        vote=Vote.UP
    )

    assert isinstance(result, VoteAlreadyCast)
    assert result.user_id == user_id
    assert result.article_id == article_id
