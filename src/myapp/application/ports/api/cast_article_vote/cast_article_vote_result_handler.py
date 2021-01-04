from __future__ import annotations

from typing import Protocol
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.ports.api.cast_article_vote.result.vote_already_cast import \
    VoteAlreadyCast


class CastArticleVoteResultHandler(Protocol):
    def handle_cast_article_vote(self, article_vote: ArticleVote):
        raise NotImplementedError()

    def handle_vote_already_cast(self, vote_already_cast: VoteAlreadyCast):
        raise NotImplementedError()

    def handle_insufficient_karma(self, user_with_insufficient_karma: UUID):
        raise NotImplementedError()
