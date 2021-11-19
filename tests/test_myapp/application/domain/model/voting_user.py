from uuid import uuid4

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


def createUserId():
    return UserId(uuid4())


def createArticleId():
    return ArticleId(uuid4())


def build_voting_user(
    user_id: UserId = createUserId(),
    voting_for_article_id: ArticleId = createArticleId(),
    voted: bool = False,
    karma: int = 10
):
    return VotingUser(
        id=user_id,
        voting_for_article_id=voting_for_article_id,
        voted=voted,
        karma=Karma(karma)
    )
