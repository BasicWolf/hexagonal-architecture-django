from typing import Optional

from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser, ArticleVote
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


def build_voting_user(
    user_id: UserId = None,
    karma: Karma = Karma(10),
    article_vote: Optional[ArticleVote] = None
) -> VotingUser:
    user_id = user_id or create_user_id()

    return VotingUser(user_id, karma, article_vote)
