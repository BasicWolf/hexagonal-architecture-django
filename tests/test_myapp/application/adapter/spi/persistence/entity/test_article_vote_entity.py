from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


def test_article_vote_entity_to_domain_model():
    article_vote = ArticleVoteEntity(
        article_id=UUID('899a9c03-0000-0000-0000-000000000000'),
        user_id=UUID('252557a2-0000-0000-0000-000000000000'),
        vote=ArticleVoteEntity.VOTE_UP
    ).to_domain_model()

    assert article_vote == ArticleVote(
        ArticleId(UUID('899a9c03-0000-0000-0000-000000000000')),
        UserId(UUID('252557a2-0000-0000-0000-000000000000')),
        Vote.UP
    )


def test_article_vote_entity_from_domain_model():
    article_vote = ArticleVote(
        ArticleId(UUID('4a463776-0000-0000-0000-000000000000')),
        UserId(UUID('d03a24ef-0000-0000-0000-000000000000')),
        Vote.DOWN
    )
    ave = ArticleVoteEntity.from_domain_model(article_vote)

    assert ave.article_id == UUID('4a463776-0000-0000-0000-000000000000')
    assert ave.user_id == UserId(UUID('d03a24ef-0000-0000-0000-000000000000'))
    assert ave.vote == ArticleVoteEntity.VOTE_DOWN
