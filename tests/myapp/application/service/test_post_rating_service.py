from unittest.mock import Mock
from uuid import UUID, uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_casting_user import VoteCastingUser
from myapp.application.ports.api.cast_article_vote.result.insufficient_karma_result import \
    InsufficientKarmaResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.get_vote_casting_user_port import GetVoteCastingUserPort
from myapp.application.service.post_rating_service import PostRatingService


def test_casting_vote_returns_casted_article_vote(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service()

    result = post_rating_service.cast_article_vote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
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


def test_casting_same_vote_two_times_returns_vote_already_cast(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        article_vote_exists_port=ArticleVoteExistsPortMock(article_exists=True)
    )

    post_rating_service.cast_article_vote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )
 
    result = post_rating_service.cast_article_vote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )

    handler = Mock()
    result.handle_by(handler)
    handler.handle_vote_already_cast.assert_called()

    # assert isinstance(result, VoteAlreadyCastResult)
    # assert result.user_id == user_id
    # assert result.article_id == article_id


def test_insufficient_karma_returned(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            user_id=user_id,
            user_karma=2
        )
    )

    result = post_rating_service.cast_article_vote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )

    assert isinstance(result, InsufficientKarmaResult)


class ArticleVoteExistsPortMock(ArticleVoteExistsPort):
    def __init__(self, article_exists=False):
        self._article_exists = article_exists

    def article_vote_exists(self, user_id: UUID, article_id: UUID):
        return self._article_exists


class GetVoteCastingUserPortMock(GetVoteCastingUserPort):
    def __init__(self, user_id: UUID = uuid4(), user_karma: int = 10):
        self.user_karma = user_karma
        self.user_id = user_id

    def get_vote_casting_user(self, user_id: UUID) -> VoteCastingUser:
        return VoteCastingUser(user_id=self.user_id, karma=self.user_karma)


def build_post_rating_service(
    article_vote_exists_port: ArticleVoteExistsPort = ArticleVoteExistsPortMock(),
    get_vote_casting_user_port: GetVoteCastingUserPort = GetVoteCastingUserPortMock()
):
    return PostRatingService(
        article_vote_exists_port=article_vote_exists_port,
        get_vote_casting_user_port=get_vote_casting_user_port
    )
