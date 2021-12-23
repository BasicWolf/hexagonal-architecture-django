from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Union

from myapp.application.domain.model.cast_article_vote_result import (
    VoteAlreadyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


class ArticleVoteProtocol(Protocol):
    @property
    def was_already_cast(self) -> bool:
        raise NotImplementedError()

    @property
    def already_cast_result(self) -> Optional[VoteAlreadyCast]:
        raise NotImplementedError()


@dataclass
class ArticleVote(ArticleVoteProtocol):
    article_id: ArticleId
    user_id: UserId
    vote: Vote

    @property
    def was_already_cast(self) -> bool:
        return True

    @property
    def already_cast_result(self) -> Optional[VoteAlreadyCast]:
        return VoteAlreadyCast(self.user_id, self.article_id)


@dataclass
class UncastArticleVote(ArticleVoteProtocol):
    article_id: ArticleId

    @property
    def was_already_cast(self) -> bool:
        return False

    @property
    def already_cast_result(self) -> Optional[VoteAlreadyCast]:
        return None


CastOrUncastArticleVote = Union[ArticleVote, UncastArticleVote]
