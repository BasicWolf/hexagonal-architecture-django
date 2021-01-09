from typing import Protocol
from uuid import UUID


class ArticleVoteExistsPort(Protocol):
    def article_vote_exists(self, user_id: UUID, article_id: UUID) -> bool:
        raise NotImplementedError()
