from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.application.adapter.api.http.problem_response import problem_response
from myapp.application.adapter.api.http.serializer.article_vote_serializer import \
    ArticleVoteSerializer
from myapp.application.adapter.api.http.serializer.cast_article_vote_command_deserializer import \
    CastArticleVoteCommandDeserializer
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    VoteCastResult, InsufficientKarmaResult, VoteAlreadyCastResult, CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import (
    CastArticleVoteUseCase
)
from myapp.application.util.assert_never import assert_never


class ArticleVoteView(APIView):
    # default `None` and # `type: ignore` for sake of .as_view()
    # which requires passed attributes to be declared on the class level :(
    cast_article_vote_use_case: CastArticleVoteUseCase = None  # type: ignore

    def __init__(self, cast_article_vote_use_case: CastArticleVoteUseCase):
        self.cast_article_vote_use_case = cast_article_vote_use_case
        super().__init__()

    def post(self, request: Request) -> Response:
        cast_article_vote_command = self._read_command(request)
        result = self.cast_article_vote_use_case.cast_article_vote(
            cast_article_vote_command
        )
        return self._build_response(result)

    def _read_command(self, request: Request) -> CastArticleVoteCommand:
        serializer = CastArticleVoteCommandDeserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.create()

    def _build_response(self, result: CastArticleVoteResult) -> Response:
        response = None

        if isinstance(result, VoteCastResult):
            response_data = ArticleVoteSerializer(result.article_vote).data
            response = Response(response_data, status=HTTPStatus.CREATED)
        elif isinstance(result, InsufficientKarmaResult):
            response = problem_response(
                title='Cannot cast a vote',
                detail=str(result),
                status=HTTPStatus.BAD_REQUEST
            )
        elif isinstance(result, VoteAlreadyCastResult):
            response = problem_response(
                title='Cannot cast a vote',
                detail=str(result),
                status=HTTPStatus.CONFLICT
            )
        else:
            assert_never(result)

        return response
