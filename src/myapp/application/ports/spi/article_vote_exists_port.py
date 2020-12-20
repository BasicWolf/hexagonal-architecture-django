from typing import Protocol
from uuid import UUID


class ArticleVoteExistsPort(Protocol):
    def article_vote_exists(self, article_id: UUID, user_id: UUID):
        raise NotImplementedError()
