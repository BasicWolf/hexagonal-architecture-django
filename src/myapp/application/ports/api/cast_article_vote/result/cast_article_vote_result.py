from __future__ import annotations

from typing import Protocol

from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import \
    CastArticleVoteResultHandler


class CastArticleVoteResult(Protocol):
    def handle_by(self, handler: CastArticleVoteResultHandler):
        raise NotImplementedError()

