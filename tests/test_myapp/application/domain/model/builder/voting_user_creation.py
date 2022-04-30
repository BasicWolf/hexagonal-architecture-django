from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


def build_voting_user(
    user_id: UserId = None,
    karma: Karma = Karma(10),
    voted: bool = False
) -> VotingUser:
    user_id = user_id or create_user_id()
    return VotingUser(user_id, karma, voted)


class VotingUserBuilder:
    def __init__(
        self,
        user_id: UserId = None,
        karma: Karma = Karma(10),
        voted: bool = False
    ):
        self.user_id = user_id
        self.karma = karma
        self.voted = voted

    def who_can_vote_for_article(self):
        return VotingUserBuilder(
            self.user_id,
            Karma(10),
            self.voted
        )

    def who_has_already_voted(self):
        return VotingUserBuilder(
            self.user_id,
            self.karma,
            True
        )

    def build(self):
        return VotingUser(
            self.user_id,
            self.karma,
            self.voted
        )
