from myapp.application.adapter.spi.persistence.model.article_vote import (
    ArticleVote as ArticleVoteDbModel
)
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.spi.save_article_vote import SaveArticleVote


class ArticleVoteRepository(
    SaveArticleVote
):
    def save_article_vote(self, article_vote: ArticleVote):
        vote = {
            Vote.UP: ArticleVoteDbModel.VOTE_UP,
            Vote.DOWN: ArticleVoteDbModel.VOTE_DOWN
        }[article_vote.vote]

        ArticleVoteDbModel(
            post_id=article_vote.post_id,
            user_id=article_vote.user_id,
            vote=vote
        ).save()
