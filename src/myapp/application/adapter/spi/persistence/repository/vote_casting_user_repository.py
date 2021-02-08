from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.vote_casting_user_entity import \
    VoteCastingUserEntity
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.get_vote_casting_user_port import GetVoteCastingUserPort


class VoteCastingUserRepository(GetVoteCastingUserPort):
    def get_vote_casting_user(self, user_id: UUID) -> VotingUser:
        entity: VoteCastingUserEntity = VoteCastingUserEntity.objects.get(id=user_id)
        return entity.to_domain_model()
