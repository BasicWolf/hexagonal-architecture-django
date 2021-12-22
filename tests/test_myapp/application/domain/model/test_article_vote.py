from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote, UncastArticleVote
from myapp.application.domain.model.cast_article_vote_result import (
    VoteAlreadyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id


def test_article_vote_has_already_cast_result():
    article_vote = ArticleVote(
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000')),
        UserId(UUID('87613e13-0000-0000-0000-000000000000')),
        Vote.DOWN
    )
    assert article_vote.was_cast_successfully
    assert article_vote.already_cast_result == VoteAlreadyCast(
        UserId(UUID('87613e13-0000-0000-0000-000000000000')),
        ArticleId(UUID('5eb18d6d-0000-0000-0000-000000000000'))
    )


def test_uncast_article_vote_already_cast_result_is_none():
    uncast_article_vote = UncastArticleVote(create_article_id())
    assert not uncast_article_vote.was_cast_successfully
    assert uncast_article_vote.already_cast_result is None
