from dataclasses import dataclass
from uuid import UUID

from myapp.application.domain.model.vote import Vote


@dataclass
class ArticleVote:
    user_id: UUID
    post_id: UUID
    vote: Vote
