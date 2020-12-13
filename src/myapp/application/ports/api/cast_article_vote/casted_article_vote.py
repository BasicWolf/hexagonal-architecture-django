from .cast_article_vote_result import CastArticleVoteResult
from .cast_article_vote_result_handler import CastArticleVoteResultHandler


class CastedArticleVote(CastArticleVoteResult):
    def handle_by(self, handler: CastArticleVoteResultHandler):
        handler.handle_casted_article_vote(self)
