from typing import Protocol

from myapp.application.domain.model.article_vote import (
    CastOrUncastArticleVote
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId


class FindArticleVotePort(Protocol):
    def find_article_vote(
            self,
            article_id: ArticleId,
            user_id: UserId
    ) -> CastOrUncastArticleVote:
        raise NotImplementedError()
