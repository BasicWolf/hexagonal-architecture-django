from dataclasses import dataclass
from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote


@dataclass
class InsufficientKarma:
    user_id: UUID


@dataclass
class VoteAlreadyCast:
    user_id: UUID
    article_id: UUID


CastVoteResult = Union[ArticleVote, InsufficientKarma, VoteAlreadyCast]
