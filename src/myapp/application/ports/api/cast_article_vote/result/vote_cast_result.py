from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import \
    CastArticleVoteResultHandler
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult


class VoteCastResult(CastArticleVoteResult):
    def __init__(self, article_vote: ArticleVote):
        self.article_vote = article_vote

    def handle_by(self, handler: CastArticleVoteResultHandler):
        handler.handle_cast_article_vote(self.article_vote)
