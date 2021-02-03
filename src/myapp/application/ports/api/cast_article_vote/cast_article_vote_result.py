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

    def __str__(self) -> str:
        return f'User {self.user_with_insufficient_karma_id} does not have ' \
                'enough karma to cast a vote'


@dataclass
class VoteAlreadyCastResult:
    cast_vote_user_id: UUID
    cast_vote_article_id: UUID

    def __str__(self) -> str:
        return f"User \"{self.cast_vote_user_id}\" has already cast a vote " \
               f"for article \"{self.cast_vote_article_id}\""


CastArticleVoteResult = Union[
    VoteCastResult,
    InsufficientKarmaResult,
    VoteAlreadyCastResult,
]
