from uuid import UUID

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import CastArticleVoteUseCase
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.casted_article_vote import \
    CastedArticleVote


class PostRatingService(
    CastArticleVoteUseCase
):

    def cast_article_vote(
        self, user_id: UUID, article_id: UUID, vote: Vote
    ) -> CastArticleVoteResult:
        return CastedArticleVote(
            ArticleVote(user_id, article_id, vote)
        )
