from uuid import UUID

from myapp.application.domain.model.voting_user import VotingUser


class GetVoteCastingUserPort:
    def get_vote_casting_user(self, user_id: UUID) -> VotingUser:
        raise NotImplementedError()
