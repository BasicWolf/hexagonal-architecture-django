from dataclasses import dataclass
from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote

MINIMUM_KARMA_REQUIRED_FOR_VOTING = 5


@dataclass
class InsufficientKarma:
    user_with_insufficient_karma_id: UUID


CastVoteResult = Union[InsufficientKarma, ArticleVote]


class VotingUser:
    id: UUID
    karma: int

    def __init__(self, id: UUID, karma: int):
        self.id = id
        self.karma = karma

    def cast_vote(self, article_id: UUID, vote: Vote) -> CastVoteResult:
        if self.karma >= MINIMUM_KARMA_REQUIRED_FOR_VOTING:
            return ArticleVote(
                user_id=self.id,
                article_id=article_id,
                vote=vote
            )
        else:
            return InsufficientKarma(user_with_insufficient_karma_id=self.id)
