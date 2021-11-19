import pytest

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import InsufficientKarma, \
    VoteAlreadyCast
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.voting_user_creation import \
    build_voting_user


@pytest.mark.parametrize('cast_vote,result_vote', [
    (Vote.UP, Vote.UP),
    (Vote.DOWN, Vote.DOWN)
])
def test_cast_vote_up_updates_user_vote(cast_vote: Vote, result_vote: Vote):
    voting_user = build_voting_user()
    voting_user.cast_vote(cast_vote)
    assert voting_user.vote == result_vote


def test_cast_vote_returns_article_vote(
    user_id: UserId,
    article_id: ArticleId
):
    voting_user = build_voting_user(
        user_id=user_id,
        voting_for_article_id=article_id,
        karma=Karma(5)
    )

    result = voting_user.cast_vote(Vote.UP)

    assert isinstance(result, ArticleVote)
    assert result.vote == Vote.UP
    assert result.article_id == article_id
    assert result.user_id == user_id


def test_cannot_cast_vote_with_insufficient_karma(user_id: UserId):
    voting_user = build_voting_user(
        user_id=user_id,
        karma=Karma(4)
    )

    result = voting_user.cast_vote(Vote.UP)

    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_cannot_cast_vote_twice(user_id: UserId, article_id: ArticleId):
    voting_user = VotingUser(
        id=user_id,
        voting_for_article_id=article_id,
        voted=True,
        karma=Karma(10)
    )

    result = voting_user.cast_vote(Vote.UP)

    assert isinstance(result, VoteAlreadyCast)
    assert result.user_id == user_id
    assert result.article_id == article_id
