from __future__ import annotations

from dataclasses import dataclass, field

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.specification.karma_enough_for_voting import (
    KarmaEnoughForVotingSpecification
)
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult,
    InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)


@dataclass()
class VotingUser:
    id: UserId
    karma: Karma
    voted_for_articles: list[ArticleId] = field(default_factory=list)

    def vote_for_article(
        self,
        article_id: ArticleId,
        vote: Vote
    ) -> VoteForArticleResult:
        if article_id in self.voted_for_articles:
            return AlreadyVotedResult(article_id, self.id)

        if not KarmaEnoughForVotingSpecification().is_satisfied_by(self.karma):
            return InsufficientKarmaResult(user_id=self.id)

        self.voted_for_articles.append(article_id)

        return SuccessfullyVotedResult(article_id, self.id, vote)
