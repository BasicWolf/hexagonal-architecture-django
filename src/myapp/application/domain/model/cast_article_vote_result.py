from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@dataclass
class InsufficientKarma:
    user_id: UserId


@dataclass
class VoteAlreadyCast:
    article_id: ArticleId
    user_id: UserId


@dataclass
class VoteSuccessfullyCast:
    article_id: ArticleId
    user_id: UserId
    vote: Vote


CastArticleVoteResult = Union[VoteSuccessfullyCast, InsufficientKarma, VoteAlreadyCast]
