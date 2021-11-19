from uuid import uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


def create_user_id():
    return UserId(uuid4())


def create_article_id():
    return ArticleId(uuid4())


def build_voting_user(
    user_id: UserId = create_user_id(),
    voting_for_article_id: ArticleId = create_article_id(),
    voted: bool = False,
    karma: int = 10
):
    return VotingUser(
        id=user_id,
        voting_for_article_id=voting_for_article_id,
        voted=voted,
        karma=Karma(karma)
    )
