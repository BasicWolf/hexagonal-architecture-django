from uuid import uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import (
    InsufficientKarma, VoteAlreadyCast,
    VoteSuccessfullyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


def test_article_vote_property_of_successfully_cast_vote():
    vote_cast_result = VoteSuccessfullyCast(
        UserId('432fedfb-0000-0000-0000-000000000000'),
        ArticleId('1aaaaaaa-0000-0000-0000-000000000000'),
        Vote.UP
    )

    assert vote_cast_result.article_vote == ArticleVote(
        ArticleId('1aaaaaaa-0000-0000-0000-000000000000'),
        UserId('432fedfb-0000-0000-0000-000000000000'),
        Vote.UP
    )


def test_vote_already_cast_result_has_no_article_vote():
    vote_already_cast = VoteAlreadyCast(UserId(uuid4()), ArticleId(uuid4()))
    assert vote_already_cast.article_vote is None


def test_insufficient_karma_result_has_no_article_vote():
    insufficient_karma = InsufficientKarma(UserId(uuid4()))
    assert insufficient_karma.article_vote is None
