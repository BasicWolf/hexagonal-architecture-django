from typing import Protocol
from uuid import UUID

from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(
        self, user_id: UUID, article_id: UUID, vote: Vote
    ) -> CastArticleVoteResult:
        raise NotImplementedError()


