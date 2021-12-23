from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import (
    InsufficientKarma,
    VoteSuccessfullyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)


def test_cast_vote_returns_expected_article_vote():
    voting_user = build_voting_user(
        UserId(UUID('24dbcd39-0000-0000-0000-000000000000'))
    )
    result_article_vote, _ = voting_user.cast_vote(
        ArticleId(UUID('aed7efd1-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert result_article_vote == ArticleVote(
        ArticleId(UUID('aed7efd1-0000-0000-0000-000000000000')),
        UserId(UUID('24dbcd39-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_cast_vote_returns_expected_cast_result():
    voting_user = build_voting_user(
        UserId(UUID('739c753c-0000-0000-0000-000000000000'))
    )

    _, cast_result = voting_user.cast_vote(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert cast_result == VoteSuccessfullyCast(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('739c753c-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_cannot_cast_vote_with_insufficient_karma(article_id: ArticleId):
    voting_user = build_voting_user(
        user_id=UserId(UUID('df777758-0000-0000-0000-000000000000')),
        karma=Karma(4)
    )

    article_vote, result = voting_user.cast_vote(article_id, Vote.UP)

    assert result == InsufficientKarma(
        UserId(UUID('df777758-0000-0000-0000-000000000000'))
    )
