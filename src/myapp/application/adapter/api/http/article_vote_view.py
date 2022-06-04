from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.application.adapter.api.http.problem_response import problem_response
from myapp.application.adapter.api.http.serializer.successfully_voted_result_serializer import (  # noqa
    SuccessfullyVotedResultSerializer
)
from myapp.application.adapter.api.http.serializer.vote_for_article_command_deserializer import (  # noqa
    VoteForArticleCommandDeserializer
)
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult,
    InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)
from myapp.application.ports.api.command.vote_for_article_command import \
    VoteForArticleCommand
from myapp.application.ports.api.vote_for_article_use_case import (
    VoteForArticleUseCase
)
from myapp.application.util.assert_never import assert_never


class ArticleVoteView(APIView):
    # default `None` and # `type: ignore` for sake of .as_view()
    # which requires passed attributes to be declared on the class level :(
    vote_for_article_use_case: VoteForArticleUseCase = None  # type: ignore

    def __init__(self, vote_for_article_use_case: VoteForArticleUseCase):
        self.vote_for_article_use_case = vote_for_article_use_case
        super().__init__()

    def post(self, request: Request) -> Response:
        vote_for_article_command = self._read_command(request)
        result = self.vote_for_article_use_case.vote_for_article(
            vote_for_article_command
        )
        return self._build_response(result)

    def _read_command(self, request: Request) -> VoteForArticleCommand:
        serializer = VoteForArticleCommandDeserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.create()

    def _build_response(self, voting_result: VoteForArticleResult) -> Response:
        response = None

        match voting_result:
            case SuccessfullyVotedResult():
                response_data = SuccessfullyVotedResultSerializer(voting_result).data
                response = Response(response_data, status=HTTPStatus.CREATED)
            case InsufficientKarmaResult(user_id):
                detail = f"User {user_id} does not have enough karma" \
                          " to vote for an article"
                response = problem_response(
                    title="Cannot vote for an article",
                    detail=detail,
                    status=HTTPStatus.BAD_REQUEST
                )
            case AlreadyVotedResult(article_id, user_id):
                detail = f"User \"{user_id}\" has already voted " \
                         f"for article \"{article_id}\""
                response = problem_response(
                    title="Cannot vote for an article",
                    detail=detail,
                    status=HTTPStatus.CONFLICT
                )
            case _:
                assert_never(voting_result)
        return response
