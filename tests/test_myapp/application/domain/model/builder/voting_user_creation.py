from typing import List

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.identifier.article_id_creation import (
    create_article_id
)
from tests.test_myapp.application.domain.model.identifier.user_id_creation import (
    create_user_id
)


def build_voting_user(
    user_id: UserId = None,
    karma: Karma = Karma(10),
    voted_for_articles: List[ArticleId] = None
) -> VotingUser:
    user_id = user_id or create_user_id()
    voted_for_articles = voted_for_articles if voted_for_articles is not None else [create_article_id()]  # noqa
    return VotingUser(user_id, karma, voted_for_articles)
