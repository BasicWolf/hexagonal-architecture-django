from uuid import UUID

from myapp.application.adapter.spi.persistence.entity.article_vote import (
    ArticleVoteEntity as ArticleVoteDbModel
)
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class ArticleVoteRepository(
    SaveArticleVotePort,
    ArticleVoteExistsPort
):
    def article_vote_exists(self, article_id: UUID, user_id: UUID):
        pass

    def save_article_vote(self, article_vote: ArticleVote):
        vote = {
            Vote.UP: ArticleVoteDbModel.VOTE_UP,
            Vote.DOWN: ArticleVoteDbModel.VOTE_DOWN
        }[article_vote.vote]

        ArticleVoteDbModel(
            article_id=article_vote.article_id,
            user_id=article_vote.user_id,
            vote=vote
        ).save()
