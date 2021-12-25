from uuid import UUID

import pytest

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult, InsufficientKarmaResult,
    SuccessfullyVotedResult
)
from tests.test_myapp.application.domain.model.builder.article_vote_creation import \
    build_article_vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)


def test_vote_for_other_than_initial_article_error(user_id, article_id):
    voting_user = build_voting_user(
        user_id,
        article_vote=build_article_vote(
            ArticleId(UUID('31d85114-0000-0000-0000-000000000000')),
            user_id,
        )
    )

    with pytest.raises(ValueError):
        voting_user.vote_for_article(article_id, Vote.DOWN)


def test_vote_for_article_twice_results_in_already_voted_result():
    voting_user = build_voting_user(
        UserId(UUID('7ebd50e7-0000-0000-0000-000000000000')),
        article_vote=ArticleVote(
            ArticleId(UUID('2f868ceb-0000-0000-0000-000000000000')),
            UserId(UUID('7ebd50e7-0000-0000-0000-000000000000')),
            Vote.DOWN
        )
    )
    result, _ = voting_user.vote_for_article(
        ArticleId(UUID('2f868ceb-0000-0000-0000-000000000000')),
        Vote.UP
    )
    assert isinstance(result, AlreadyVotedResult)


def test_vote_for_article_returns_expected_article_vote():
    voting_user = build_voting_user(
        UserId(UUID('24dbcd39-0000-0000-0000-000000000000'))
    )
    _, article_vote_result = voting_user.vote_for_article(
        ArticleId(UUID('aed7efd1-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert article_vote_result == ArticleVote(
        ArticleId(UUID('aed7efd1-0000-0000-0000-000000000000')),
        UserId(UUID('24dbcd39-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_vote_for_article_returns_successfully_voted_result():
    voting_user = build_voting_user(
        UserId(UUID('739c753c-0000-0000-0000-000000000000'))
    )

    voting_result, _ = voting_user.vote_for_article(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert voting_result == SuccessfullyVotedResult(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('739c753c-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_cannot_vote_for_article_with_insufficient_karma(article_id: ArticleId):
    voting_user = build_voting_user(
        user_id=UserId(UUID('df777758-0000-0000-0000-000000000000')),
        karma=Karma(4)
    )

    result, article_vote = voting_user.vote_for_article(article_id, Vote.UP)

    assert result == InsufficientKarmaResult(
        UserId(UUID('df777758-0000-0000-0000-000000000000'))
    )


def test_construct_voting_user_with_article_vote_of_different_user_error():
    with pytest.raises(ValueError):
        build_voting_user(
            user_id=UserId(UUID('c9e851c2-0000-0000-0000-000000000000')),
            article_vote=ArticleVote(
                ArticleId(UUID('f8ca014b-0000-0000-0000-000000000000')),
                UserId(UUID('412fad29-0000-0000-0000-000000000000')),
                Vote.DOWN
            )
        )
