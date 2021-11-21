from typing import Optional

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import InsufficientKarma, \
    VoteAlreadyCast, CastArticleVoteResult
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote


class VotingUser:
    id: UserId
    karma: Karma
    _article_vote: Optional[ArticleVote]

    def __init__(
        self,
        id: UserId,
        karma: Karma,
        article_vote: Optional[ArticleVote] = None
    ):
        self.id = id
        self.karma = karma
        self._article_vote = article_vote

    def cast_vote(self, article_id: ArticleId, vote: Vote) -> CastArticleVoteResult:
        if self.voted:
            return VoteAlreadyCast(
                user_id=self.id,
                article_id=article_id
            )

        if not self.karma.enough_for_voting():
            return InsufficientKarma(user_id=self.id)

        self._article_vote = ArticleVote(
            user_id=self.id,
            article_id=article_id,
            vote=vote
        )

        return self._article_vote

    @property
    def article_vote(self):
        return self._article_vote

    @property
    def voted(self):
        return self.article_vote is not None
