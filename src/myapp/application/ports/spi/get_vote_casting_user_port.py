from uuid import UUID

from myapp.application.domain.model.vote_casting_user import VoteCastingUser


class GetVoteCastingUserPort:
    def get_vote_casting_user(self, user_id: UUID) -> VoteCastingUser:
        raise NotImplementedError()
