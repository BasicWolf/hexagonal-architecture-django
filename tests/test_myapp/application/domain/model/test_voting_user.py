from uuid import UUID

from myapp.application.domain.event.user_voted_event import UserVotedEvent
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
        voted=True
    )
    result, *_ = voting_user.vote_for_article(
        ArticleId(UUID('2f868ceb-0000-0000-0000-000000000000')),
        Vote.UP
    )
    assert isinstance(result, AlreadyVotedResult)


def test_vote_for_article_returns_successfully_voted_result():
    voting_user = build_voting_user(
        UserId(UUID('739c753c-0000-0000-0000-000000000000'))
    )

    voting_result, *_ = voting_user.vote_for_article(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        Vote.DOWN
    )

    assert voting_result == SuccessfullyVotedResult(
        ArticleId(UUID('4df32c92-0000-0000-0000-000000000000')),
        UserId(UUID('739c753c-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_vote_for_article_returns_one_event():
    voting_user = build_voting_user(
        UserId(UUID('18d068a1-0000-0000-0000-000000000000'))
    )

    *_, events = voting_user.vote_for_article(
        ArticleId(UUID('f5376f8d-0000-0000-0000-000000000000')),
        Vote.UP
    )

    assert len(events) == 1


def test_vote_for_article_returns_user_voted_event():
    voting_user = build_voting_user(
        UserId(UUID('bcc249f7-0000-0000-0000-000000000000'))
    )

    *_, events = voting_user.vote_for_article(
        ArticleId(UUID('d9d1e906-0000-0000-0000-000000000000')),
        Vote.UP
    )

    event = events[0]
    assert isinstance(event, UserVotedEvent)
    assert event.article_id == ArticleId(UUID('d9d1e906-0000-0000-0000-000000000000'))
    assert event.user_id == ArticleId(UUID('bcc249f7-0000-0000-0000-000000000000'))
    assert event.vote == Vote.UP


def test_cannot_vote_for_article_with_insufficient_karma(article_id: ArticleId):
    voting_user = build_voting_user(
        user_id=UserId(UUID('df777758-0000-0000-0000-000000000000')),
        karma=Karma(4)
    )

    result, article_vote, *_ = voting_user.vote_for_article(article_id, Vote.UP)

    assert result == InsufficientKarmaResult(
        UserId(UUID('df777758-0000-0000-0000-000000000000'))
    )
