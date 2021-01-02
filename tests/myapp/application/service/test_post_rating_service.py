from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.casted_article_vote import \
    CastedArticleVote
from myapp.application.ports.api.cast_article_vote.vote_already_cast_result import \
    VoteAlreadyCastResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
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

    assert isinstance(result, CastedArticleVote)
    assert result.article_vote == ArticleVote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
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

    assert isinstance(result, VoteAlreadyCastResult)
    assert result.user_id == user_id
    assert result.article_id == article_id


def test_insufficient_karma_returned(
    user_id: UUID, article_id: UUID
):
    pass


class ArticleVoteExistsPortMock(ArticleVoteExistsPort):
    def __init__(self, article_exists=False):
        self._article_exists = article_exists

    def article_vote_exists(self, user_id: UUID, article_id: UUID):
        return self._article_exists


def build_post_rating_service(
    article_vote_exists_port: ArticleVoteExistsPort = ArticleVoteExistsPortMock()
):
    return PostRatingService(
        article_vote_exists_port=article_vote_exists_port
    )
