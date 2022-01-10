from typing import Protocol

from myapp.application.ports.spi.dto.article_vote import ArticleVote


class SaveArticleVotePort(Protocol):
    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        raise NotImplementedError()
