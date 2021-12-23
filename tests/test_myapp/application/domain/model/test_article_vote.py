from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import (
    VoteAlreadyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


def test_article_vote_has_already_cast_result():
    article_vote = ArticleVote(
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000')),
        UserId(UUID('87613e13-0000-0000-0000-000000000000')),
        Vote.DOWN
    )
    assert article_vote.to_vote_already_cast_result() == VoteAlreadyCast(
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000')),
        UserId(UUID('87613e13-0000-0000-0000-000000000000'))
    )
