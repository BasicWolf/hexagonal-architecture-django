from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class VotingUser:
    id: UserId
    karma: Karma

    def cast_vote(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> Tuple[CastArticleVoteResult, Optional[ArticleVote]]:
        if not self.karma.enough_for_voting():
            return  InsufficientKarma(user_id=self.id), None

        return (
            VoteSuccessfullyCast(article_id, self.id, vote),
            ArticleVote(article_id, self.id, vote)
        )
