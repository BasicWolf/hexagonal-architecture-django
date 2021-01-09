from typing import Protocol

from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    CastArticleVoteResult


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        raise NotImplementedError()


