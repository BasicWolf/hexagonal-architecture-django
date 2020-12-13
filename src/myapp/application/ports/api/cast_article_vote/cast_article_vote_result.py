from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .cast_article_vote_result_handler import CastArticleVoteResultHandler


class CastArticleVoteResult(Protocol):
    def handle_by(self, handler: CastArticleVoteResultHandler):
        raise NotImplementedError()
