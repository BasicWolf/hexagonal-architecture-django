from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, TYPE_CHECKING, Union

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote

if TYPE_CHECKING:
    from myapp.application.domain.model.article_vote import ArticleVote


class CastArticleVoteResultProtocol(Protocol):
    @property
    def article_vote(self) -> Optional[ArticleVote]:
        raise NotImplementedError()


@dataclass
class InsufficientKarma(CastArticleVoteResultProtocol):
    user_id: UserId

    @property
    def article_vote(self) -> Optional[ArticleVote]:
        return None


@dataclass
class VoteAlreadyCast(CastArticleVoteResultProtocol):
    user_id: UserId
    article_id: ArticleId

    @property
    def article_vote(self) -> Optional[ArticleVote]:
        return None


@dataclass
class VoteSuccessfullyCast(CastArticleVoteResultProtocol):
    user_id: UserId
    article_id: ArticleId
    vote: Vote

    @property
    def article_vote(self) -> Optional[ArticleVote]:
        from myapp.application.domain.model.article_vote import ArticleVote
        return ArticleVote(self.article_id, self.user_id, self.vote)


CastArticleVoteResult = Union[VoteSuccessfullyCast, InsufficientKarma, VoteAlreadyCast]
