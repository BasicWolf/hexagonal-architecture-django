from typing import Optional
from uuid import uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.command.vote_for_article_command import (
    VoteForArticleCommand
)


def build_vote_for_article_command(
    article_id: Optional[ArticleId] = None,
    user_id: Optional[UserId] = None,
    vote: Vote = Vote.UP
) -> VoteForArticleCommand:
    return VoteForArticleCommand(
        article_id or ArticleId(uuid4()),
        user_id or UserId(uuid4()),
        vote
    )
