from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id
from tests.test_myapp.application.domain.model.identifier.user_id_creation import \
    create_user_id


def build_voting_user(
    user_id: UserId = None,
    voting_for_article_id: ArticleId = None,
    voted: bool = False,
    karma: int = 10
):
    user_id = user_id or create_user_id()
    voting_for_article_id = voting_for_article_id or create_article_id()

    return VotingUser(
        id=user_id,
        voting_for_article_id=voting_for_article_id,
        voted=voted,
        karma=Karma(karma)
    )
