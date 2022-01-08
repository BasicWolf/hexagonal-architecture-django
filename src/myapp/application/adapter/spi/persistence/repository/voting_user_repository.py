from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort


class VotingUserRepository(
    FindVotingUserPort
):
    def find_voting_user(self, article_id: ArticleId, user_id: UserId) -> VotingUser:
        voting_user_entity = self._get_voting_user_entity(user_id)
        voting_user_entity.voted = self._get_user_voted_for_article(article_id, user_id)
        return voting_user_entity.to_domain_model()

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            # Annotations can be used to add `voted` field to the returned result,
            # but we want to keep things simple and clear.
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e

    def _get_user_voted_for_article(
        self,
        article_id: ArticleId,
        user_id: UserId
    ) -> bool:
        return ArticleVoteEntity.objects.filter(
            article_id=article_id,
            user_id=user_id
        ).exists()
