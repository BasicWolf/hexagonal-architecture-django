from dataclasses import dataclass
from typing import Protocol

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import VoteForArticleResult


@dataclass
class VoteForArticleCommand:
    article_id: ArticleId
    user_id: UserId
    vote: Vote


class VoteForArticleUseCase(Protocol):
    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        raise NotImplementedError()
