from dataclasses import dataclass, field
from uuid import UUID, uuid4

from myapp.application.domain.model.vote import Vote


@dataclass
class ArticleVote:
    user_id: UUID
    article_id: UUID
    vote: Vote
    id: UUID = field(default_factory=uuid4)
