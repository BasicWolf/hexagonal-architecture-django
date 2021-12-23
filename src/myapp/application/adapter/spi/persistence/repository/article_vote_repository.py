from typing import Optional

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.domain.model.article_vote import (
    ArticleVote
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.ports.spi.find_article_vote_port import FindArticleVotePort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class ArticleVoteRepository(
    FindArticleVotePort,
    SaveArticleVotePort
):
    def find_article_vote(
        self,
        article_id: ArticleId,
        user_id: UserId
    ) -> Optional[ArticleVote]:
        found_article_vote_entity = ArticleVoteEntity.objects.filter(
            article_id=article_id,
            user_id=user_id
        ).first()

        if found_article_vote_entity is None:
            return None
        else:
            return found_article_vote_entity.to_domain_model()

    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        article_vote_entity = ArticleVoteEntity.from_domain_model(article_vote)
        article_vote_entity.save()
        return article_vote_entity.to_domain_model()
