from dataclasses import dataclass
from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.user_id import UserId


@dataclass
class InsufficientKarma:
    user_id: UserId


@dataclass
class VoteAlreadyCast:
    user_id: UserId
    article_id: UUID


CastArticleVoteResult = Union[ArticleVote, InsufficientKarma, VoteAlreadyCast]
