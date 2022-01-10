from typing import Optional

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.spi.dto.article_vote import ArticleVote
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


def build_article_vote(
    article_id: Optional[ArticleId] = None,
    user_id: Optional[UserId] = None,
    vote: Vote = Vote.UP
) -> ArticleVote:
    article_id = article_id or create_article_id()
    user_id = user_id or create_user_id()

    return ArticleVote(article_id, user_id, vote)
