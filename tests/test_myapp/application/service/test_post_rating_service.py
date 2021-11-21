from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import VoteAlreadyCast, \
    InsufficientKarma
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_voting_user_port import SaveVotingUserPort
from myapp.application.service.post_rating_service import PostRatingService
from tests.test_myapp.application.domain.model.article_vote import build_article_vote
from tests.test_myapp.application.domain.model.voting_user_creation import \
    build_voting_user


def test_casting_valid_vote_returns_result(
    user_id: UserId,
    article_id: ArticleId
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=FindVotingUserPortStub(
            build_voting_user(user_id=user_id)
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    assert isinstance(result, ArticleVote)
    assert result == ArticleVote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )


def test_casting_same_vote_two_times_returns_vote_already_cast_result(
    user_id: UserId,
    article_id: ArticleId
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=FindVotingUserPortStub(
            build_voting_user(
                user_id=user_id,
                article_vote=build_article_vote(user_id=user_id, vote=Vote.UP)
            )
        )
    )
 
    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    assert isinstance(result, VoteAlreadyCast)
    assert result.user_id == user_id
    assert result.article_id == article_id


def test_casting_vote_returns_insufficient_karma_result(
    user_id: UserId,
    article_id: ArticleId
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=FindVotingUserPortStub(
            returned_vote_casting_user=build_voting_user(
                user_id=user_id,
                karma=Karma(2)
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )
    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_voting_user_saved(
    user_id: UserId,
    article_id: ArticleId
):
    save_voting_user_port_mock = SaveVotingUserPortMock()
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=FindVotingUserPortStub(
            returned_vote_casting_user=build_voting_user(
                user_id=user_id,
                karma=Karma(21)
            )
        ),
        save_voting_user_port=save_voting_user_port_mock
    )

    post_rating_service.cast_article_vote(
        CastArticleVoteCommand(
            user_id,
            article_id,
            Vote.DOWN
        )
    )

    saved_voting_user = save_voting_user_port_mock.saved_voting_user
    assert saved_voting_user.id == user_id
    assert saved_voting_user.karma == Karma(21)


class FindVotingUserPortStub(FindVotingUserPort):
    def __init__(
        self,
        returned_vote_casting_user: VotingUser = build_voting_user()
    ):
        self.returned_vote_casting_user = returned_vote_casting_user

    def find_voting_user(self, user_id: UserId, article_id: UUID) -> VotingUser:
        return self.returned_vote_casting_user


class SaveVotingUserPortMock(SaveVotingUserPort):
    saved_voting_user: VotingUser

    def save_voting_user(self, voting_user: VotingUser) -> VotingUser:
        self.saved_voting_user = voting_user
        return voting_user


def build_post_rating_service(
    get_vote_casting_user_port: FindVotingUserPort = FindVotingUserPortStub(),
    save_voting_user_port: SaveVotingUserPort = SaveVotingUserPortMock()
):
    return PostRatingService(
        find_voting_user_port=get_vote_casting_user_port,
        save_voting_user_port=save_voting_user_port
    )
