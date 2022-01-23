from dataclasses import dataclass

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class VoteForArticleCommand:
    article_id: ArticleId
    user_id: UserId
    vote: Vote
