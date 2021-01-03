from typing import Union
from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote

MINIMUM_KARMA_REQUIRED_FOR_VOTING = 5


class InsufficientKarma:
    pass


CastVoteResult = Union[InsufficientKarma, ArticleVote]


class VoteCastingUser:
    user_id: UUID
    karma: int

    def __init__(self, user_id: UUID, karma: int):
        self.user_id = user_id
        self.karma = karma

    def cast_vote(self, article_id: UUID, vote: Vote) -> CastVoteResult:
        if self.karma >= MINIMUM_KARMA_REQUIRED_FOR_VOTING:
            return ArticleVote(
                user_id=self.user_id,
                article_id=article_id,
                vote=vote
            )
        else:
            return InsufficientKarma()
