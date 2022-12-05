from myapp.application.adapter.spi.persistence.entity.article_vote_entity import (
    ArticleVoteEntity
)
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import (
    VotingUserEntity
)

# A way to explicitly tell linters that the imported classes are used
__all__ = [
    'ArticleVoteEntity',
    'VotingUserEntity'
]
