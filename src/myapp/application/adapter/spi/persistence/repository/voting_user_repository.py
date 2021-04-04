from uuid import UUID

from django.db.models import Exists

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.get_voting_user_port import GetVotingUserPort


class VotingUserRepository(GetVotingUserPort):
    def get_voting_user(self, user_id: UUID, article_id: UUID) -> VotingUser:
        annotated_entity = VotingUserEntity.objects\
            .annotate(
                voted=Exists(
                    ArticleVoteEntity.objects.filter(
                        user_id=user_id,
                        article_id=article_id
                    )
                )
            ).get(id=user_id)

        return self._to_domain_model(annotated_entity, voting_for_article_id=article_id)

    def _to_domain_model(self, entity, voting_for_article_id: UUID) -> VotingUser:
        return VotingUser(
            id=entity.id,
            voting_for_article_id=voting_for_article_id,
            voted=entity.voted,
            karma=entity.karma
        )
