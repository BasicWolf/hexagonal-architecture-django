from typing import Optional
from unittest.mock import patch
from uuid import UUID

import pytest

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import SuccessfullyVotedResult
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.command.vote_for_article_command import (
    VoteForArticleCommand
)
from myapp.application.ports.spi.dto.article_vote import ArticleVote
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.article_rating_service import ArticleRatingService
from tests.test_myapp.application.port.api.command.builder.vote_for_article_command_creation import (  # noqa
    build_vote_for_article_command
)


@pytest.fixture
def atomic_transactions_noop_stub_for_article_service():
    with patch(f'{ArticleRatingService.__module__}.transaction.atomic'):
        yield


@pytest.mark.usefixtures("atomic_transactions_noop_stub_for_article_service")
class TestArticleRatingService:
    def test_successfully_voted_for_article(
        self,
        vote_for_article_command: VoteForArticleCommand,
        successfully_voted_result: SuccessfullyVotedResult
    ):
        article_rating_service = build_article_rating_service()

        vote_for_article_result = article_rating_service.vote_for_article(
            vote_for_article_command
        )

        assert vote_for_article_result == successfully_voted_result

    def test_article_vote_saved(
        self,
        vote_for_article_command: VoteForArticleCommand,
        saved_article_vote: ArticleVote
    ):
        save_article_vote_port_mock = SaveArticleVotePortMock()
        article_rating_service = build_article_rating_service(
            save_article_vote_port=save_article_vote_port_mock
        )

        article_rating_service.vote_for_article(vote_for_article_command)

        assert save_article_vote_port_mock.saved_article_vote == saved_article_vote


class FindVotingUserPortStub(FindVotingUserPort):
    def find_voting_user(self, article_id: ArticleId, user_id: UserId) -> VotingUser:
        return VotingUser(user_id, Karma(10))


class SaveArticleVotePortMock(SaveArticleVotePort):
    def __init__(self):
        self.saved_article_vote: Optional[ArticleVote] = None

    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        self.saved_article_vote = article_vote
        return article_vote


@pytest.fixture(scope='module')
def vote_for_article_command() -> VoteForArticleCommand:
    return VoteForArticleCommand(
        ArticleId(UUID('c77fc6c4-0000-0000-0000-000000000000')),
        UserId(UUID('bd971243-0000-0000-0000-000000000000')),
        Vote.UP
    )


@pytest.fixture(scope='module')
def saved_article_vote() -> ArticleVote:
    return ArticleVote(
        ArticleId(UUID('c77fc6c4-0000-0000-0000-000000000000')),
        UserId(UUID('bd971243-0000-0000-0000-000000000000')),
        Vote.UP
    )


@pytest.fixture(scope='module')
def successfully_voted_result() -> SuccessfullyVotedResult:
    return SuccessfullyVotedResult(
        ArticleId(UUID('c77fc6c4-0000-0000-0000-000000000000')),
        UserId(UUID('bd971243-0000-0000-0000-000000000000')),
        Vote.UP
    )


def build_article_rating_service(
    find_voting_user_port: FindVotingUserPort = FindVotingUserPortStub(),
    save_article_vote_port: SaveArticleVotePort = SaveArticleVotePortMock(),
):
    return ArticleRatingService(
        find_voting_user_port,
        save_article_vote_port
    )
