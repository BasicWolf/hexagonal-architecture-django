from __future__ import annotations

from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote


class InsufficientKarmaResult:
    user_with_insufficient_karma_id: UUID

    def __init__(self, user_with_insufficient_karma_id: UUID):
        self.user_with_insufficient_karma_id = user_with_insufficient_karma_id

    def __str__(self) -> str:
        return f'User {self.user_with_insufficient_karma_id} does not have ' \
                'enough karma to cast a vote'


class VoteAlreadyCastResult:
    cast_vote_user_id: UUID
    cast_vote_article_id: UUID

    def __init__(self, user_id: UUID, article_id: UUID):
        self.cast_vote_user_id = user_id
        self.cast_vote_article_id = article_id

    def __str__(self) -> str:
        return f"User \"{self.cast_vote_user_id}\" has already cast a vote " \
               f"for article \"{self.cast_vote_article_id}\""


class VoteCastResult:
    def __init__(self, article_vote: ArticleVote):
        self.article_vote = article_vote


CastArticleVoteResult = Union[
    InsufficientKarmaResult,
    VoteAlreadyCastResult,
    VoteCastResult,
]

