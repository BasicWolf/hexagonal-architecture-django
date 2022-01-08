from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from myapp.application.domain.event.user_voted_event import UserVotedEvent
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
    voted: bool

    def vote_for_article(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> Tuple[VoteForArticleResult, List[Event]]:
        if self.voted:
            return AlreadyVotedResult(article_id, self.id), []
        if not self.karma.enough_for_voting():
            return InsufficientKarmaResult(user_id=self.id), []

        self.voted = True

        return (
            SuccessfullyVotedResult(article_id, self.id, vote),
            [
                UserVotedEvent(article_id, self.id, vote)
            ]
        )
