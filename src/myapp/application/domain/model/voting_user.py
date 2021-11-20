from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import InsufficientKarma, \
    VoteAlreadyCast, CastArticleVoteResult
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote


class VotingUser:
    id: UserId
    voting_for_article_id: ArticleId
    vote: Vote
    karma: Karma

    def __init__(
        self,
        id: UserId,
        voting_for_article_id: ArticleId,
        karma: Karma,
        vote: Vote = Vote.NOT_VOTED
    ):
        self.id = id
        self.voting_for_article_id = voting_for_article_id
        self.karma = karma
        self.vote = vote

    def cast_vote(self, vote: Vote) -> CastArticleVoteResult:
        if self.voted:
            return VoteAlreadyCast(
                user_id=self.id,
                article_id=self.voting_for_article_id
            )

        if not self.karma.enough_for_voting():
            return InsufficientKarma(user_id=self.id)

        self.vote = vote

        return ArticleVote(
            user_id=self.id,
            article_id=self.voting_for_article_id,
            vote=vote
        )

    @property
    def voted(self):
        return self.vote != Vote.NOT_VOTED
