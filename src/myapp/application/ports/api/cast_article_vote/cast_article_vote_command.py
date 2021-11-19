from dataclasses import dataclass
from uuid import UUID

from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class CastArticleVoteCommand:
    user_id: UserId
    article_id: UUID
    vote: Vote
