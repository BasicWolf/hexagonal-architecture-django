from __future__ import annotations

from dataclasses import dataclass
from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote


@dataclass
class VoteCastResult:
    article_vote: ArticleVote


@dataclass
class InsufficientKarmaResult:
    user_with_insufficient_karma_id: UUID


@dataclass
class VoteAlreadyCastResult:
    cast_vote_user_id: UUID
    cast_vote_article_id: UUID


CastArticleVoteResult = Union[
    VoteCastResult,
    InsufficientKarmaResult,
    VoteAlreadyCastResult,
]
