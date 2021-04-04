from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote


def test_build_article_vote_entity_from_domain_model(
    user_id: UUID,
    article_id: UUID,
    article_vote_id: UUID,
):
    article_vote = ArticleVote(
        id=article_vote_id,
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )

    ave: ArticleVoteEntity = ArticleVoteEntity.from_domain_model(article_vote)
    assert ave.id == article_vote_id
    assert ave.user_id == user_id
    assert ave.article_id == article_id
    assert ave.vote == ArticleVoteEntity.VOTE_UP


def test_article_vote_entity_to_domain_model(
    user_id: UUID,
    article_id: UUID,
    article_vote_id: UUID,
):
    article_vote_entity = ArticleVoteEntity(
        id=article_vote_id,
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_DOWN
    )

    assert article_vote_entity.to_domain_model() == ArticleVote(
        id=article_vote_id,
        user_id=user_id,
        article_id=article_id,
        vote=Vote.DOWN
    )
