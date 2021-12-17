from uuid import uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class ArticleVoteRepository(SaveArticleVotePort):
    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        return ArticleVote(
            ArticleId(uuid4()),
            UserId(uuid4()),
            Vote.UP
        )
