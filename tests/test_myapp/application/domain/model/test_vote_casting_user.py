from uuid import uuid4

import pytest

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser, \
    InsufficientKarma


@pytest.mark.parametrize(
    'karma', [5, 10]
)
def test_cast_vote_returns_article_vote(user_id, article_id, karma):
    vote_casting_user = VotingUser(
        id=user_id,
        karma=10
    )

    result = vote_casting_user.cast_vote(
        article_id=article_id,
        vote=Vote.UP
    )

    assert isinstance(result, ArticleVote)
    assert result.vote == Vote.UP
    assert result.article_id == article_id
    assert result.user_id == user_id


def test_cannot_cast_vote_with_insufficient_karma(user_id):
    vote_casting_user = VotingUser(
        id=user_id,
        karma=4
    )

    result = vote_casting_user.cast_vote(
        article_id=uuid4(),
        vote=Vote.UP
    )

    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id
