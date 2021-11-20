import pytest

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import InsufficientKarma, \
    VoteAlreadyCast
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
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


def test_casting_vote_returns_already_cast():
    voting_user = build_voting_user(
        user_id=UserId('476820aa-d91f-4ab8-8743-6f6f4c5047d0'),
        voting_for_article_id=ArticleId('d07af0ab-0576-4c10-b361-6587fee6a837'),
        vote=Vote.UP
    )

    result = voting_user.cast_vote(Vote.DOWN)

    assert isinstance(result, VoteAlreadyCast)
    assert result.user_id == UserId('476820aa-d91f-4ab8-8743-6f6f4c5047d0')
    assert result.article_id == ArticleId('d07af0ab-0576-4c10-b361-6587fee6a837')


@pytest.mark.parametrize(
    'vote', [Vote.UP, Vote.DOWN]
)
def test_cannot_cast_vote_twice(vote: Vote):
    voting_user = build_voting_user(vote=Vote.UP)

    result = voting_user.cast_vote(vote)

    assert isinstance(result, VoteAlreadyCast)
