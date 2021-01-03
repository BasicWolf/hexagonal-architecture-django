from uuid import UUID

from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import \
    CastArticleVoteResultHandler
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.result.vote_already_cast import \
    VoteAlreadyCast


class VoteAlreadyCastResult(CastArticleVoteResult):

    def __init__(self, user_id: UUID, article_id: UUID):
        self._vote_already_cast = VoteAlreadyCast(
            user_id=user_id,
            article_id=article_id
        )

    def handle_by(self, handler: CastArticleVoteResultHandler):
        handler.handle_vote_already_cast(self._vote_already_cast)
