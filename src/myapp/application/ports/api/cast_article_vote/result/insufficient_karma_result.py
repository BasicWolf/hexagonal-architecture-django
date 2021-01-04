from uuid import UUID

from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import \
    CastArticleVoteResultHandler
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult


class InsufficientKarmaResult(CastArticleVoteResult):
    _user_with_insufficient_karma_id: UUID

    def __init__(self, user_with_insufficient_karma_id: UUID):
        self._user_with_insufficient_karma_id = user_with_insufficient_karma_id

    def handle_by(self, handler: CastArticleVoteResultHandler):
        handler.handle_insufficient_karma(self._user_with_insufficient_karma_id)

