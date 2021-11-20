from uuid import uuid4

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


def test_build_article_vote_entity_from_domain_model(
    user_id: UserId,
    article_id: ArticleId,
):
    article_vote = ArticleVote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )

    ave: ArticleVoteEntity = ArticleVoteEntity.from_domain_model(article_vote)
    assert ave.user_id == user_id
    assert ave.article_id == article_id
    assert ave.vote == ArticleVoteEntity.VOTE_UP


def test_article_vote_entity_to_domain_model(
    user_id: UserId,
    article_id: ArticleId,
):
    article_vote_entity = ArticleVoteEntity(
        id=uuid4(),
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_DOWN
    )

    assert article_vote_entity.to_domain_model() == ArticleVote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.DOWN
    )
