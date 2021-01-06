from uuid import UUID

from rest_framework.views import APIView

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result_handler import (
    CastArticleVoteResultHandler
)
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import (
    CastArticleVoteUseCase
)
from myapp.application.ports.api.cast_article_vote.result.vote_already_cast import (
    VoteAlreadyCast
)


class ArticleVoteController(CastArticleVoteResultHandler, APIView):
    def __init__(self, cast_article_vote_use_case: CastArticleVoteUseCase):
        self._cast_article_vote_use_case = cast_article_vote_use_case

    def post(self, request):
        pass

    def handle_cast_article_vote(self, article_vote: ArticleVote):
        pass

    def handle_vote_already_cast(self, vote_already_cast: VoteAlreadyCast):
        pass

    def handle_insufficient_karma(self, user_with_insufficient_karma: UUID):
        pass
