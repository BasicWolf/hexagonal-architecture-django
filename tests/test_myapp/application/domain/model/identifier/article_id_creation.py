from uuid import UUID, uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId


def create_article_id(*args, **kwargs):
    if args or kwargs:
        return ArticleId(UUID(*args, **kwargs))
    else:
        return ArticleId(uuid4())
