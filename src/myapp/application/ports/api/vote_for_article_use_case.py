from typing import Protocol

from myapp.application.domain.model.vote_for_article_result import VoteForArticleResult
from myapp.application.ports.api.command.vote_for_article_command import \
    VoteForArticleCommand


class VoteForArticleUseCase(Protocol):
    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        raise NotImplementedError()
