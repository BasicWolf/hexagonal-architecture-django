from dataclasses import dataclass

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class CastArticleVoteCommand:
    user_id: UserId
    article_id: ArticleId
    vote: Vote
