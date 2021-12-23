from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort


class VotingUserRepository(
    FindVotingUserPort
):
    def find_voting_user(self, user_id: UserId) -> VotingUser:
        voting_user_entity = self._get_voting_user_entity(user_id)
        return VotingUser(
            id=UserId(voting_user_entity.user_id),
            karma=Karma(voting_user_entity.karma)
        )

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e
