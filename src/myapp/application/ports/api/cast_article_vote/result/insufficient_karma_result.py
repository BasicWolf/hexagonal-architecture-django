from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import \
    CastArticleVoteResultHandler
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult


class InsufficientKarmaResult(CastArticleVoteResult):
    def handle_by(self, handler: CastArticleVoteResultHandler):
        pass

