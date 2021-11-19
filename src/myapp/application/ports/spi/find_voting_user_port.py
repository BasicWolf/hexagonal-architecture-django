from typing import Protocol
from uuid import UUID

from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.voting_user import VotingUser


class FindVotingUserPort(Protocol):
    def find_voting_user(self, user_id: UserId, article_id: UUID) -> VotingUser:
        raise NotImplementedError()
