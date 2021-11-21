from dataclasses import dataclass
from typing import Protocol

from myapp.application.domain.model.cast_article_vote_result import CastArticleVoteResult
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class CastArticleVoteCommand:
    user_id: UserId
    article_id: ArticleId
    vote: Vote


class CastArticleVoteUseCase(Protocol):
    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        raise NotImplementedError()


