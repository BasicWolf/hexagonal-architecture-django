from dataclasses import dataclass
from typing import Union

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId


@dataclass
class InsufficientKarma:
    user_id: UserId


@dataclass
class VoteAlreadyCast:
    user_id: UserId
    article_id: ArticleId


CastArticleVoteResult = Union[ArticleVote, InsufficientKarma, VoteAlreadyCast]
