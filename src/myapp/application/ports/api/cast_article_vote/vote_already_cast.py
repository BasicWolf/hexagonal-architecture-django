from dataclasses import dataclass
from uuid import UUID


@dataclass
class VoteAlreadyCast:
    user_id: UUID
    article_id: UUID
