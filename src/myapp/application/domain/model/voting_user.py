from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from myapp.application.domain.model.article_vote import (
    ArticleVote
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)


@dataclass
class VotingUser:
    id: UserId
    karma: Karma
    article_vote: Optional[ArticleVote] = None

    def vote_for_article(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> Tuple[VoteForArticleResult, Optional[ArticleVote]]:
        if not self.karma.enough_for_voting():
            return (
                InsufficientKarmaResult(user_id=self.id),
                None
            )

        self.article_vote = ArticleVote(
            article_id,
            self.id,
            vote
        )

        return (
            SuccessfullyVotedResult(article_id, self.id, vote),
            ArticleVote(article_id, self.id, vote)
        )
