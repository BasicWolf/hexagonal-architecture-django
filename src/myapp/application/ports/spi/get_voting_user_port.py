from typing import Protocol
from uuid import UUID

from myapp.application.domain.model.voting_user import VotingUser


class GetVotingUserPort(Protocol):
    def get_voting_user(self, user_id: UUID, article_id: UUID) -> VotingUser:
        raise NotImplementedError()
