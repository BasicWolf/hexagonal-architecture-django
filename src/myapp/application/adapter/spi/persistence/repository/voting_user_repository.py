from django.db.models import Exists

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
from django.db.models import Exists

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


class VotingUserRepository(FindVotingUserPort):
    def find_voting_user(self, user_id: UserId, article_id: ArticleId) -> VotingUser:
        try:
            annotated_entity = VotingUserEntity.objects\
                .annotate(
                    voted=Exists(
                        ArticleVoteEntity.objects.filter(
                            user_id=user_id,
                            article_id=article_id
                        )
                    )
                ).get(id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e

        return self._to_domain_model(annotated_entity, voting_for_article_id=article_id)

    def _to_domain_model(self, entity, voting_for_article_id: ArticleId) -> VotingUser:
        return VotingUser(
            id=UserId(entity.id),
            voting_for_article_id=voting_for_article_id,
            voted=entity.voted,
            karma=entity.karma
        )
