from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    InsufficientKarmaResult,
    SuccessfullyVotedResult
)
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)


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
