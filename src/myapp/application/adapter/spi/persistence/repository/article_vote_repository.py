from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import (
    ArticleVoteEntity
)
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class ArticleVoteRepository(
    SaveArticleVotePort,
    ArticleVoteExistsPort
):
    def article_vote_exists(self, user_id: UUID, article_id: UUID) -> bool:
        return ArticleVoteEntity.objects.filter(
            article_id=article_id,
            user_id=user_id
        ).exists()

    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        article_vote_entity = ArticleVoteEntity.from_domain_model(article_vote)
        article_vote_entity.save()
        return article_vote_entity.to_domain_model()
