from uuid import UUID

from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import CastArticleVoteUseCase
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import CastArticleVoteResult


class PostRatingService(
    CastArticleVoteUseCase
):

    def cast_article_vote(
        self, user_id: UUID, post_id: UUID, vote: Vote
    ) -> CastArticleVoteResult:
        return
