from typing import Protocol

from .cast_article_vote_command import  CastArticleVoteCommand
from .cast_article_vote_result import CastArticleVoteResult


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        raise NotImplementedError()
