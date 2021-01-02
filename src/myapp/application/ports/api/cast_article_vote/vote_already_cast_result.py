from uuid import UUID

from .cast_article_vote_result import CastArticleVoteResult
from .cast_article_vote_result_handler import CastArticleVoteResultHandler


class VoteAlreadyCastResult(CastArticleVoteResult):
    user_id: UUID
    article_id: UUID

    def __init__(self, user_id: UUID, article_id: UUID):
        self.user_id = user_id
        self.article_id = article_id

    def handle_by(self, handler: CastArticleVoteResultHandler):
        raise NotImplementedError()
