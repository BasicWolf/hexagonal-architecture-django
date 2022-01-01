from typing import Optional
from uuid import UUID

from myapp.application.domain.event.user_voted_event import UserVotedEvent
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult,
    InsufficientKarmaResult,
    SuccessfullyVotedResult
)
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.vote_for_article_use_case import \
    VoteForArticleCommand
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.article_rating_service import ArticleRatingService
from myapp.eventlib.event_dispatcher import EventDispatcher
from tests.test_myapp.application.domain.model.builder.article_vote_creation import \
    build_article_vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)
from tests.test_myapp.eventlib.intercepting_event_dispatcher import \
    InterceptingEventDispatcher


def test_valid_vote_for_article_returns_result(
    user_id: UserId,
    article_id: ArticleId
):
    article_rating_service = build_article_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            build_voting_user(user_id=user_id)
        )
    )

    result = article_rating_service.vote_for_article(
        VoteForArticleCommand(article_id, user_id, Vote.UP)
    )

    assert isinstance(result, SuccessfullyVotedResult)
    assert result == SuccessfullyVotedResult(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )


def test_voting_for_article_two_times_returns_already_voted_result():
    article_rating_service = build_article_rating_service(
        FindVotingUserPortStub(
            build_voting_user(
                user_id=UserId(UUID('912997c2-0000-0000-0000-000000000000')),
                article_vote=build_article_vote(
                    ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
                    UserId(UUID('912997c2-0000-0000-0000-000000000000'))
                )
            )
        )
    )

    result = article_rating_service.vote_for_article(
        VoteForArticleCommand(
            ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
            UserId(UUID('912997c2-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )

    assert result == AlreadyVotedResult(
        ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
        UserId(UUID('912997c2-0000-0000-0000-000000000000'))
    )


def test_voting_for_article_returns_insufficient_karma_result(
    user_id: UserId,
    article_id: ArticleId
):
    article_rating_service = build_article_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            returned_voting_user=build_voting_user(
                user_id=user_id,
                karma=Karma(2)
            )
        )
    )

    result = article_rating_service.vote_for_article(
        VoteForArticleCommand(article_id, user_id, Vote.UP)
    )
    assert isinstance(result, InsufficientKarmaResult)
    assert result.user_id == user_id


def test_article_vote_saved_when_user_voted_event_handled():
    save_article_vote_port_mock = SaveArticleVotePortMock()
    article_rating_service = build_article_rating_service(
        save_article_vote_port=save_article_vote_port_mock
    )

    article_rating_service._on_user_voted(
        UserVotedEvent(
            ArticleId(UUID('dd329c97-0000-0000-0000-000000000000')),
            UserId(UUID('896ca302-0000-0000-0000-000000000000')),
            Vote.DOWN
        )
    )

    assert save_article_vote_port_mock.saved_article_vote == ArticleVote(
        ArticleId(UUID('dd329c97-0000-0000-0000-000000000000')),
        UserId(UUID('896ca302-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_vote_for_article_twice_does_not_save_the_vote():
    save_article_vote_port_mock = SaveArticleVotePortMock()
    article_rating_service = build_article_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            returned_voting_user=build_voting_user(
                user_id=UserId(UUID('4110f0fc-0000-0000-0000-000000000000')),
                article_vote=ArticleVote(
                    ArticleId(UUID('b63b6490-0000-0000-0000-000000000000')),
                    UserId(UUID('4110f0fc-0000-0000-0000-000000000000')),
                    Vote.UP
                )
            )
        ),
        save_article_vote_port=save_article_vote_port_mock
    )

    article_rating_service.vote_for_article(
        VoteForArticleCommand(
            ArticleId(UUID('b63b6490-0000-0000-0000-000000000000')),
            UserId(UUID('4110f0fc-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )

    assert save_article_vote_port_mock.saved_article_vote is None


def test_vote_for_article_dispatches_user_voted_event():
    intercepting_event_dispatcher = InterceptingEventDispatcher()
    article_rating_service = build_article_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            returned_voting_user=build_voting_user(
                user_id=UserId(UUID('c0d1bc64-0000-0000-0000-000000000000')),
                article_vote=None
            )
        ),
        domain_event_dispatcher=intercepting_event_dispatcher
    )

    article_rating_service.vote_for_article(
        VoteForArticleCommand(
            ArticleId(UUID('2a43f4e5-0000-0000-0000-000000000000')),
            UserId(UUID('c0d1bc64-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )

    assert intercepting_event_dispatcher.check_event_dispatched(
        UserVotedEvent(
            ArticleId(UUID('2a43f4e5-0000-0000-0000-000000000000')),
            UserId(UUID('c0d1bc64-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )


def test_article_rating_service_registered_as_user_created_event_handler():
    event_dispatcher = EventDispatcher()
    article_rating_service = build_article_rating_service(
        domain_event_dispatcher=event_dispatcher
    )
    assert event_dispatcher.get_handlers_for(UserVotedEvent) == [
        article_rating_service._on_user_voted
    ]


class FindVotingUserPortStub(FindVotingUserPort):
    def __init__(
        self,
        returned_voting_user: Optional[VotingUser] = None
    ):
        returned_voting_user = returned_voting_user or build_voting_user()
        self.returned_voting_user = returned_voting_user

    def find_voting_user(self, article_id: ArticleId, user_id: UserId) -> VotingUser:
        return self.returned_voting_user


class SaveArticleVotePortMock(SaveArticleVotePort):
    saved_article_vote: Optional[ArticleVote] = None

    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        self.saved_article_vote = article_vote
        return article_vote


def build_article_rating_service(
    find_voting_user_port: FindVotingUserPort = FindVotingUserPortStub(),
    save_article_vote_port: SaveArticleVotePort = SaveArticleVotePortMock(),
    domain_event_dispatcher: EventDispatcher = EventDispatcher()
):
    return ArticleRatingService(
        find_voting_user_port,
        save_article_vote_port,
        domain_event_dispatcher
    )
