from dataclasses import dataclass
from typing import Optional, Protocol, Union

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


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
        return ArticleVote(self.article_id, self.vote)


CastArticleVoteResult = Union[VoteSuccessfullyCast, InsufficientKarma, VoteAlreadyCast]
