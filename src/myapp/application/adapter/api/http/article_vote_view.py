from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.application.adapter.api.http.serializer.cast_article_vote_command_serializer import \
    CastArticleVoteCommandSerializer
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


class ArticleVoteView(CastArticleVoteResultHandler, APIView):
    def __init__(self, cast_article_vote_use_case: CastArticleVoteUseCase):
        super().__init__()
        self._cast_article_vote_use_case = cast_article_vote_use_case

    def post(self, request: Request):
        serializer = CastArticleVoteCommandSerializer(data=request.data)
        cast_article_vote_command = serializer.create()

        cast_article_vote_result = self._cast_article_vote_use_case.cast_article_vote(
            cast_article_vote_command
        )
        return cast_article_vote_result.handle_by(self)

    def handle_cast_article_vote(self, article_vote: ArticleVote):
        return Response({}, status=status.HTTP_201_CREATED)

    def handle_vote_already_cast(self, vote_already_cast: VoteAlreadyCast):
        pass

    def handle_insufficient_karma(self, user_with_insufficient_karma: UUID):
        pass
