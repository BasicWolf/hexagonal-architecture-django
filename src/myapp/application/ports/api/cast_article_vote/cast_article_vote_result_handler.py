from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from casted_article_vote import CastedArticleVote


class CastArticleVoteResultHandler(Protocol):
    def handle_casted_article_vote(self, casted_article_vote: 'CastedArticleVote'):
        raise NotImplementedError()
