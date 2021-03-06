from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import VoteAlreadyCast, \
    InsufficientKarma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.spi.get_voting_user_port import GetVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.post_rating_service import PostRatingService
from tests.test_myapp.application.domain.model.voting_user import build_voting_user


def test_casting_valid_vote_returns_result(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVotingUserPortMock(
            build_voting_user(
                user_id=user_id,
                voting_for_article_id=article_id
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    assert isinstance(result, ArticleVote)
    assert result == ArticleVote(
        id=result.id,
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )


def test_casting_same_vote_two_times_returns_vote_already_cast_result(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVotingUserPortMock(
            build_voting_user(
                user_id=user_id,
                voting_for_article_id=article_id,
                voted=True
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
    user_id: UUID,
    article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVotingUserPortMock(
            returned_vote_casting_user=build_voting_user(
                user_id=user_id,
                karma=2
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )
    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_cast_vote_created(
    user_id: UUID,
    article_id: UUID
):
    save_article_vote_port_mock = SaveArticleVotePortMock()
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVotingUserPortMock(
            returned_vote_casting_user=build_voting_user(
                user_id=user_id,
                voting_for_article_id=article_id
            )
        ),
        save_article_vote_port=save_article_vote_port_mock
    )

    post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.DOWN)
    )

    saved_article_vote = save_article_vote_port_mock.saved_article_vote
    assert saved_article_vote.user_id == user_id
    assert saved_article_vote.article_id == article_id
    assert saved_article_vote.vote == Vote.DOWN


class GetVotingUserPortMock(GetVotingUserPort):
    def __init__(
        self,
        returned_vote_casting_user: VotingUser = build_voting_user()
    ):
        self.returned_vote_casting_user = returned_vote_casting_user

    def get_voting_user(self, user_id: UUID, article_id: UUID) -> VotingUser:
        return self.returned_vote_casting_user


class SaveArticleVotePortMock(SaveArticleVotePort):
    saved_article_vote = None

    def save_article_vote(self, article_vote: ArticleVote):
        self.saved_article_vote = article_vote


def build_post_rating_service(
    get_vote_casting_user_port: GetVotingUserPort = GetVotingUserPortMock(),
    save_article_vote_port: SaveArticleVotePort = SaveArticleVotePortMock()
):
    return PostRatingService(
        get_voting_user_port=get_vote_casting_user_port,
        save_article_vote_port=save_article_vote_port
    )
