from __future__ import annotations

from dataclasses import dataclass

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


class VoteForArticleResult:
    pass


@dataclass
class InsufficientKarmaResult(VoteForArticleResult):
    user_id: UserId


@dataclass
class AlreadyVotedResult(VoteForArticleResult):
    article_id: ArticleId
    user_id: UserId


@dataclass
class SuccessfullyVotedResult(VoteForArticleResult):
    article_id: ArticleId
    user_id: UserId
    vote: Vote
