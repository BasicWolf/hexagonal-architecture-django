from uuid import uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.article_vote_id import ArticleVoteId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from tests.test_myapp.application.domain.model.voting_user import createUserId, \
    createArticleId


def build_article_vote(
    id: ArticleVoteId = None,
    user_id: UserId = None,
    article_id: ArticleId = None,
    vote: Vote = Vote.UP
) -> ArticleVote:
    id = id or create_article_vote_id()
    user_id = user_id or createUserId()
    article_id = article_id or createArticleId()

    return ArticleVote(
        id=id,
        user_id=user_id,
        article_id=article_id,
        vote=vote
    )


def create_article_vote_id() -> ArticleVoteId:
    return ArticleVoteId(uuid4())
