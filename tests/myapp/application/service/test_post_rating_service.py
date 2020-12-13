from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.casted_article_vote import \
    CastedArticleVote
from myapp.application.service.post_rating_service import PostRatingService


def test_casting_vote_returns_expected_cast_article_vote_result():
    result = PostRatingService().cast_article_vote(
        user_id=UUID('fff0c0bf-ec3c-433a-9dc6-a1f9524f19b4'),
        post_id=UUID('18287c9a-93a8-46a8-ae20-781cf36b4352'),
        vote=Vote.UP
    )

    assert isinstance(result, CastedArticleVote)
    assert result.article_vote == ArticleVote(
        user_id=UUID('fff0c0bf-ec3c-433a-9dc6-a1f9524f19b4'),
        post_id=UUID('18287c9a-93a8-46a8-ae20-781cf36b4352'),
        vote=Vote.UP
    )
