import pytest
from http import HTTPStatus
from uuid import uuid4

from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.vote_for_article_result import (
    VoteForArticleResult,
)
from myapp.application.port.api.command.vote_for_article_command import (
    VoteForArticleCommand
)
from myapp.application.port.api.vote_for_article_use_case import (
    VoteForArticleUseCase
)


def test__when_making_malformed_request__return_http_bad_request(
    post_article_vote_with_missing_data
):
    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=VoteForArticleUseCaseNoopStub()
    )

    response = post_article_vote_with_missing_data(article_vote_view)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == {
        'vote': [
            ErrorDetail("This field is required.", code='required')
        ]
    }


@pytest.fixture
def post_article_vote_with_missing_data(arf: APIRequestFactory):
    def _post_article_vote_with_missing_data(article_vote_view) -> Response:
        return article_vote_view(
            arf.post(
                '/article_vote',
                {
                    'user_id': str(uuid4()),
                    'article_id': str(uuid4())
                },
                format='json'
            )
        )
    return _post_article_vote_with_missing_data


class VoteForArticleUseCaseNoopStub(VoteForArticleUseCase):
    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        raise Exception("This should never be reached - we should fail earlier")
