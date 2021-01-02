from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import CastArticleVoteUseCase
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.casted_article_vote import CastedArticleVote
from myapp.application.ports.api.cast_article_vote.vote_already_cast_result import VoteAlreadyCastResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort


class PostRatingService(
    CastArticleVoteUseCase
):
    def __init__(
        self,
        article_vote_exists_port: ArticleVoteExistsPort
    ):
        self._article_vote_exists_port = article_vote_exists_port

    def cast_article_vote(
        self, user_id: UUID, article_id: UUID, vote: Vote
    ) -> CastArticleVoteResult:
        if self._article_vote_exists_port.article_vote_exists(
            user_id=user_id,
            article_id=article_id
        ):
            return VoteAlreadyCastResult(
                user_id=user_id,
                article_id=article_id
            )

        return CastedArticleVote(
            ArticleVote(user_id, article_id, vote)
        )
