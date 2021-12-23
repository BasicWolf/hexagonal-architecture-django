from __future__ import annotations

from dataclasses import dataclass

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


class CastArticleVoteResult:
    pass


@dataclass
class InsufficientKarma(CastArticleVoteResult):
    user_id: UserId


@dataclass
class VoteAlreadyCast(CastArticleVoteResult):
    article_id: ArticleId
    user_id: UserId


@dataclass
class VoteSuccessfullyCast(CastArticleVoteResult):
    article_id: ArticleId
    user_id: UserId
    vote: Vote
