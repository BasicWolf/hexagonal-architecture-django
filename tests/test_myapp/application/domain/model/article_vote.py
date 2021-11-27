from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import ArticleVote
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


