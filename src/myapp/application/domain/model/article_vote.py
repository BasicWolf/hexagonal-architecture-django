from dataclasses import dataclass, field
from uuid import uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.article_vote_id import ArticleVoteId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class ArticleVote:
    user_id: UserId
    article_id: ArticleId
    vote: Vote
    id: ArticleVoteId = field(
        default_factory=lambda: ArticleVoteId(uuid4())
    )
