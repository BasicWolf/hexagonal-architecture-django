from uuid import UUID

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult, InsufficientKarmaResult,
    SuccessfullyVotedResult
)
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)


def test_vote_for_article_twice_returns_already_voted_result():
    voting_user = build_voting_user(
        UserId(UUID('7ebd50e7-0000-0000-0000-000000000000')),
        voted_for_articles=[ArticleId(UUID('2f868ceb-0000-0000-0000-000000000000'))]
    )
    result = voting_user.vote_for_article(
        ArticleId(UUID('2f868ceb-0000-0000-0000-000000000000')),
        Vote.UP
    )
    assert isinstance(result, AlreadyVotedResult)


def test_vote_for_article_returns_successfully_voted_result():
    voting_user = build_voting_user(
        UserId(UUID('739c753c-0000-0000-0000-000000000000'))
    )

    voting_result = voting_user.vote_for_article(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert voting_result == SuccessfullyVotedResult(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('739c753c-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_cannot_vote_for_article_with_insufficient_karma(an_article_id: ArticleId):
    voting_user = build_voting_user(
        user_id=UserId(UUID('df777758-0000-0000-0000-000000000000')),
        karma=Karma(4)
    )

    result = voting_user.vote_for_article(an_article_id, Vote.UP)

    assert result == InsufficientKarmaResult(
        UserId(UUID('df777758-0000-0000-0000-000000000000'))
    )
