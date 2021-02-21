from typing import Protocol

from myapp.application.domain.model.cast_vote_result import CastVoteResult
from .cast_article_vote_command import CastArticleVoteCommand


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastVoteResult:
        raise NotImplementedError()
