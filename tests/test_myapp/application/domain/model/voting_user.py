from uuid import UUID, uuid4

from myapp.application.domain.model.voting_user import VotingUser


def build_voting_user(
    user_id: UUID = uuid4(),
    voting_for_article_id: UUID = uuid4(),
    voted: bool = False,
    karma: int = 10
):
    return VotingUser(
        id=user_id,
        voting_for_article_id=voting_for_article_id,
        voted=voted,
        karma=karma
    )
