from __future__ import annotations

from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.ports.api.cast_article_vote.vote_already_cast import \
    VoteAlreadyCast


class InsufficientKarmaResult:
    user_with_insufficient_karma_id: UUID

    def __init__(self, user_with_insufficient_karma_id: UUID):
        self.user_with_insufficient_karma_id = user_with_insufficient_karma_id


class VoteAlreadyCastResult:
    vote_already_cast: VoteAlreadyCast

    def __init__(self, user_id: UUID, article_id: UUID):
        self.vote_already_cast = VoteAlreadyCast(
            user_id=user_id,
            article_id=article_id
        )


class VoteCastResult:
    def __init__(self, article_vote: ArticleVote):
        self.article_vote = article_vote


CastArticleVoteResult = Union[
    InsufficientKarmaResult,
    VoteAlreadyCastResult,
    VoteCastResult,
]

