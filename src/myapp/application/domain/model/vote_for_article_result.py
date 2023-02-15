from __future__ import annotations

from dataclasses import dataclass

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


class VoteForArticleResult:
    def to_message(self) -> str:
        raise NotImplementedError()


@dataclass
class InsufficientKarmaResult(VoteForArticleResult):
    user_id: UserId

    def to_message(self) -> str:
        return f"User {self.user_id} does not have enough karma" \
                 " to vote for an article"


@dataclass
class AlreadyVotedResult(VoteForArticleResult):
    article_id: ArticleId
    user_id: UserId

    def to_message(self) -> str:
        return f"User \"{self.user_id}\" has already voted " \
                 f"for article \"{self.article_id}\""


@dataclass
class SuccessfullyVotedResult(VoteForArticleResult):
    article_id: ArticleId
    user_id: UserId
    vote: Vote
