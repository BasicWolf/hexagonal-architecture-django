from typing import Protocol

from myapp.application.domain.model.cast_article_vote_result import CastArticleVoteResult
from .cast_article_vote_command import CastArticleVoteCommand


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        raise NotImplementedError()
