from __future__ import annotations

from dataclasses import dataclass, field

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult,
    InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)

MINIMUM_KARMA_REQUIRED_FOR_VOTING = Karma(5)


@dataclass
class VotingUser:
    id: UserId
    karma: Karma
    votes_for_articles: list[ArticleVote] = field(default_factory=list)

    def vote_for_article(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> VoteForArticleResult:
        if self._user_voted_for_article(article_id):
            return AlreadyVotedResult(article_id, self.id)

        if not self._karma_enough_for_voting():
            return InsufficientKarmaResult(user_id=self.id)

        self.votes_for_articles.append(
            ArticleVote(article_id, self.id, vote)
        )

        return SuccessfullyVotedResult(article_id, self.id, vote)

    def _karma_enough_for_voting(self):
        return self.karma >= MINIMUM_KARMA_REQUIRED_FOR_VOTING

    def _user_voted_for_article(self, article_id: ArticleId) -> bool:
        article_ids_for_which_user_voted = (
            article_vote.article_id for article_vote in self.votes_for_articles
        )
        return article_id in article_ids_for_which_user_voted


@dataclass
class ArticleVote:
    article_id: ArticleId
    user_id: UserId
    vote: Vote
