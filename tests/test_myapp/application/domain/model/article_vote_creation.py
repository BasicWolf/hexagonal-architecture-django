from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.vote import Vote
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id


def build_article_vote(
    article_id: ArticleId = None,
    vote: Vote = Vote.UP
) -> ArticleVote:
    article_id = article_id or create_article_id()

    return ArticleVote(
        article_id=article_id,
        vote=vote
    )
