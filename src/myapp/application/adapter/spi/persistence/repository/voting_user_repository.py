from typing import Optional

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort


class VotingUserRepository(
    FindVotingUserPort
):
    def find_voting_user(self, article_id: ArticleId, user_id: UserId) -> VotingUser:
        voting_user_entity = self._get_voting_user_entity(user_id)
        article_vote = self._find_article_vote(article_id, user_id)
        return voting_user_entity.to_domain_model(article_vote)

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e

    def _find_article_vote(
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



