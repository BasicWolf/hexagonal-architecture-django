from uuid import uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId


def create_article_id():
    return ArticleId(uuid4())
