from uuid import UUID

import pytest

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult, InsufficientKarmaResult,
    SuccessfullyVotedResult
)
from myapp.application.domain.model.voting_user import ArticleVote, VotingUser


def test_vote_for_article_twice_returns_already_voted_result(
    voting_user_who_has_voted: VotingUser,
    article_id_for_which_user_has_voted: ArticleId,
    a_vote: Vote,
    expected_already_voted_result: AlreadyVotedResult
):
    voting_result = voting_user_who_has_voted.vote_for_article(
        article_id_for_which_user_has_voted,
        a_vote
    )
    assert voting_result == expected_already_voted_result


def test_vote_for_article_returns_successfully_voted_result(
    voting_user_who_has_not_voted: VotingUser,
    article_id_for_which_user_has_voted: ArticleId,
    expected_successfully_voted_result: SuccessfullyVotedResult
):
    voting_result = voting_user_who_has_not_voted.vote_for_article(
        article_id_for_which_user_has_voted,
        Vote.DOWN
    )

    assert voting_result == expected_successfully_voted_result


def test_cannot_vote_for_article_with_insufficient_karma(
    voting_user_with_insufficient_karma_for_voting: VotingUser,
    an_article_id: ArticleId,
    a_vote: Vote,
    expected_insufficient_karma_result: InsufficientKarmaResult
):
    voting_result = voting_user_with_insufficient_karma_for_voting.vote_for_article(
        an_article_id,
        a_vote
    )

    assert voting_result == expected_insufficient_karma_result


@pytest.fixture(scope='module')
def article_id_for_which_user_has_voted() -> ArticleId:
    return ArticleId(UUID('4df32c92-0000-0000-0000-000000000000'))


@pytest.fixture(scope='module')
def voting_user_who_has_voted() -> VotingUser:
    return VotingUser(
        UserId(UUID('7ebd50e7-0000-0000-0000-000000000000')),
        Karma(10),
        [
            ArticleVote(
                ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
                UserId(UUID('7ebd50e7-0000-0000-0000-000000000000')),
                Vote.DOWN
            )
        ]
    )


@pytest.fixture(scope='module')
def expected_already_voted_result() -> AlreadyVotedResult:
    return AlreadyVotedResult(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('7ebd50e7-0000-0000-0000-000000000000'))
    )


@pytest.fixture(scope='module')
def voting_user_who_has_not_voted() -> VotingUser:
    return VotingUser(
        UserId(UUID('c23ec6da-0000-0000-0000-000000000000')),
        Karma(10),
        []
    )


@pytest.fixture(scope='module')
def expected_successfully_voted_result() -> SuccessfullyVotedResult:
    return SuccessfullyVotedResult(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('c23ec6da-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


@pytest.fixture(scope='module')
def voting_user_with_insufficient_karma_for_voting() -> VotingUser:
    return VotingUser(
        UserId(UUID('d826bff6-0000-0000-0000-000000000000')),
        Karma(4),
        []
    )


@pytest.fixture(scope='module')
def expected_insufficient_karma_result() -> InsufficientKarmaResult:
    return InsufficientKarmaResult(
        UserId(UUID('d826bff6-0000-0000-0000-000000000000'))
    )
