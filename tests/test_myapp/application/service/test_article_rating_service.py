from typing import List, Optional
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

from myapp.application.domain.event.user_voted_event import UserVotedEvent
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    SuccessfullyVotedResult, VoteForArticleResult
)
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.command.vote_for_article_command import \
    VoteForArticleCommand
from myapp.application.ports.spi.dto.article_vote import ArticleVote
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.article_rating_service import ArticleRatingService
from myapp.eventlib.event import Event
from myapp.eventlib.event_dispatcher import EventDispatcher
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)
from tests.test_myapp.application.port.api.command.builder.vote_for_article_command_creation import (  # noqa
    build_vote_for_article_command
)
from tests.test_myapp.eventlib.intercepting_event_dispatcher import (
    InterceptingEventDispatcher
)


@pytest.fixture
def atomic_transactions_noop_stub_for_article_service():
    with patch(f'{ArticleRatingService.__module__}.transaction.atomic'):
        yield


@pytest.mark.usefixtures("atomic_transactions_noop_stub_for_article_service")
class TestArticleRatingService:
    def test_arguments_passed_to_find_voting_user(self):
        find_voting_user_port_mock = MagicMock()
        find_voting_user_port_mock.find_voting_user = MagicMock(
            return_value = build_voting_user_mock()
        )
        article_rating_service = build_article_rating_service(
            find_voting_user_port_mock
        )

        article_rating_service.vote_for_article(
            VoteForArticleCommand(
                ArticleId(UUID('8e048172-0000-0000-0000-000000000000')),
                UserId(UUID('bb9e0560-0000-0000-0000-000000000000')),
                Vote.DOWN
            )
        )
        find_voting_user_port_mock.find_voting_user.assert_called_with(
            ArticleId(UUID('8e048172-0000-0000-0000-000000000000')),
            UserId(UUID('bb9e0560-0000-0000-0000-000000000000'))
        )

    def test_arguments_passed_to_vote_for_article(self):
        found_voting_user_mock = build_voting_user_mock()

        article_rating_service = build_article_rating_service(
            FindVotingUserPortStub(found_voting_user_mock)
        )
        article_rating_service.vote_for_article(
            build_vote_for_article_command(
                article_id=ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
                vote=Vote.UP
            )
        )

        found_voting_user_mock.vote_for_article.assert_called_with(
            ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
            Vote.UP
        )

    def test_domain_events_dispatched(self):
        found_voting_user_mock = build_voting_user_mock(
            returned_events=[
                UserVotedEvent(
                    article_id=ArticleId(UUID('58093339-0000-0000-0000-000000000000')),
                    user_id=UserId(UUID('193d88c7-0000-0000-0000-000000000000')),
                    vote=Vote.DOWN
                )
            ]
        )

        intercepting_event_dispatcher = InterceptingEventDispatcher()

        article_rating_service = build_article_rating_service(
            find_voting_user_port=FindVotingUserPortStub(found_voting_user_mock),
            domain_event_dispatcher=intercepting_event_dispatcher
        )

        article_rating_service.vote_for_article(build_vote_for_article_command())

        assert intercepting_event_dispatcher.dispatched_events == [
            UserVotedEvent(
                article_id=ArticleId(UUID('58093339-0000-0000-0000-000000000000')),
                user_id=UserId(UUID('193d88c7-0000-0000-0000-000000000000')),
                vote=Vote.DOWN
            )
        ]

    def test_article_vote_saved_when_user_voted_event_handled(self):
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

    def test_article_rating_service_registered_as_user_created_event_handler(self):
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


def build_voting_user_mock(
    returned_result: Optional[VoteForArticleResult] = None,
    returned_events: Optional[List[Event]] = None
) -> MagicMock:
    if returned_result is None:
        returned_result = SuccessfullyVotedResult(
            ArticleId(uuid4()),
            UserId(uuid4()),
            Vote.UP
        )
    if returned_events is None:
        returned_events = []

    user_mock = MagicMock()
    user_mock.vote_for_article = MagicMock()
    user_mock.vote_for_article.return_value = (returned_result, returned_events)
    return user_mock


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
