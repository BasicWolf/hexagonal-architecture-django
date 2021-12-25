from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult
)


def test_article_vote_has_already_voted_result():
    article_vote = ArticleVote(
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000')),
        UserId(UUID('87613e13-0000-0000-0000-000000000000')),
        Vote.DOWN
    )
    assert article_vote.to_already_voted_result() == AlreadyVotedResult(
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000')),
        UserId(UUID('87613e13-0000-0000-0000-000000000000'))
    )
