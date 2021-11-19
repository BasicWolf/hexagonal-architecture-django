from uuid import uuid4

from myapp.application.domain.model.identifier.article_vote_id import ArticleVoteId


def create_article_vote_id() -> ArticleVoteId:
    return ArticleVoteId(uuid4())
