from typing import Protocol

from myapp.application.domain.model.article_vote import ArticleVote


class SaveArticleVotePort(Protocol):
    def save_article_vote(self, article_vote: ArticleVote):
        raise NotImplementedError()
