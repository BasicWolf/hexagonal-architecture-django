from __future__ import annotations

from typing import Optional, Tuple

from myapp.application.domain.model.article_vote import (
    ArticleVote
)
from myapp.application.domain.model.cast_article_vote_result import (
    CastArticleVoteResult,
    InsufficientKarma,
    VoteSuccessfullyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote


class VotingUser:
    id: UserId
    karma: Karma

    def __init__(
        self,
        id: UserId,
        karma: Karma,
    ):
        self.id = id
        self.karma = karma

    def cast_vote(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> Tuple[Optional[ArticleVote], CastArticleVoteResult]:
        if not self.karma.enough_for_voting():
            return None, InsufficientKarma(user_id=self.id)

        return (
            ArticleVote(article_id, self.id, vote),
            VoteSuccessfullyCast(self.id, article_id, vote)
        )
