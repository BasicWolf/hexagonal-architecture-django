from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import InsufficientKarma, \
    VoteAlreadyCast, CastArticleVoteResult
from myapp.application.domain.model.vote import Vote

MINIMUM_KARMA_REQUIRED_FOR_VOTING = 5


class VotingUser:
    id: UUID
    voting_for_article_id: UUID
    voted: bool
    karma: int

    def __init__(
        self,
        id: UUID,
        voting_for_article_id: UUID,
        voted: bool,
        karma: int
    ):
        self.id = id
        self.voting_for_article_id = voting_for_article_id
        self.voted = voted
        self.karma = karma

    def cast_vote(self, vote: Vote) -> CastArticleVoteResult:
        if self.voted:
            return VoteAlreadyCast(
                user_id=self.id,
                article_id=self.voting_for_article_id
            )

        if self.karma < MINIMUM_KARMA_REQUIRED_FOR_VOTING:
            return InsufficientKarma(user_id=self.id)

        self.voted = True

        return ArticleVote(
            user_id=self.id,
            article_id=self.voting_for_article_id,
            vote=vote
        )
