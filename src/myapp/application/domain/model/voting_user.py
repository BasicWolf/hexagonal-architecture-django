from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from myapp.application.domain.event.user_voted_event import UserVotedEvent
from myapp.application.domain.model.article_vote import (
    ArticleVote
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult, InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)
from myapp.eventlib.event import Event


@dataclass
class VotingUser:
    id: UserId
    karma: Karma
    article_vote: Optional[ArticleVote] = None

    def __post_init__(self):
        if (
            self.article_vote is not None
            and self.article_vote.user_id != UserId(self.id)
        ):
            raise ValueError("Invalid state: Article Vote does not belong to the user")

    def vote_for_article(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> Tuple[VoteForArticleResult, List[Event]]:
        if (
            self.article_vote is not None
            and self.article_vote.article_id != article_id
        ):
            raise ValueError("Invalid state: A user can't re-vote for an article with"
                             " a different id")

        if self.article_vote is not None:
            return AlreadyVotedResult(article_id, self.id), []

        if not self.karma.enough_for_voting():
            return InsufficientKarmaResult(user_id=self.id), []

        self.article_vote = ArticleVote(
            article_id,
            self.id,
            vote
        )

        return (
            SuccessfullyVotedResult(article_id, self.id, vote),
            [
                UserVotedEvent(article_id, self.id, vote)
            ]
        )
