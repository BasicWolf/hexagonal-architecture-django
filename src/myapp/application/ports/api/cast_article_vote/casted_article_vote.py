from myapp.application.domain.model.article_vote import ArticleVote
from .cast_article_vote_result import CastArticleVoteResult
from .cast_article_vote_result_handler import CastArticleVoteResultHandler


class CastedArticleVote(CastArticleVoteResult):
    def __init__(self, article_vote: ArticleVote):
        self.article_vote = article_vote

    def handle_by(self, handler: CastArticleVoteResultHandler):
        handler.handle_casted_article_vote(self)
