from unittest.mock import Mock
from uuid import UUID, uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_casting_user import VoteCastingUser
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.result.vote_already_cast import \
    VoteAlreadyCast
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.get_vote_casting_user_port import GetVoteCastingUserPort
from myapp.application.service.post_rating_service import PostRatingService


def test_casting_valid_vote_invokes_handler(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            build_vote_casting_user(user_id=user_id)
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    handler = Mock()
    result.handle_by(handler)

    handler.handle_cast_article_vote.assert_called_with(
        ArticleVote(
            user_id=user_id,
            article_id=article_id,
            vote=Vote.UP
        )
    )


def test_casting_same_vote_two_times_invokes_vote_already_cast_handler(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        article_vote_exists_port=ArticleVoteExistsPortMock(article_exists=True)
    )
 
    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    handler = Mock()
    result.handle_by(handler)
    handler.handle_vote_already_cast.assert_called_with(
        VoteAlreadyCast(user_id, article_id)
    )


def test_casting_vote_invokes_insufficient_karma_handler(
    user_id: UUID,
    article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            returned_vote_casting_user=VoteCastingUser(
                user_id=user_id,
                karma=2
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    result_handler_mock = Mock()
    result.handle_by(result_handler_mock)
    result_handler_mock.handle_insufficient_karma.assert_called_with(user_id)


class ArticleVoteExistsPortMock(ArticleVoteExistsPort):
    def __init__(self, article_exists=False):
        self._article_exists = article_exists

    def article_vote_exists(self, user_id: UUID, article_id: UUID):
        return self._article_exists


def build_vote_casting_user(user_id: UUID = uuid4(), karma: int = 10):
    return VoteCastingUser(user_id=user_id, karma=karma)


class GetVoteCastingUserPortMock(GetVoteCastingUserPort):
    def __init__(
        self,
        returned_vote_casting_user: VoteCastingUser = build_vote_casting_user()
    ):
        self.returned_vote_casting_user = returned_vote_casting_user

    def get_vote_casting_user(self, user_id: UUID) -> VoteCastingUser:
        return self.returned_vote_casting_user


def build_post_rating_service(
    article_vote_exists_port: ArticleVoteExistsPort = ArticleVoteExistsPortMock(),
    get_vote_casting_user_port: GetVoteCastingUserPort = GetVoteCastingUserPortMock()
):
    return PostRatingService(
        article_vote_exists_port=article_vote_exists_port,
        get_vote_casting_user_port=get_vote_casting_user_port
    )
