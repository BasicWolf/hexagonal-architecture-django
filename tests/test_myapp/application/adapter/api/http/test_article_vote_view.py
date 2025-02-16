from http import HTTPStatus

from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote_for_article_result import (
    VoteForArticleResult,
)
from myapp.application.port.api.command.vote_for_article_command import (
    VoteForArticleCommand
)
from myapp.application.port.api.vote_for_article_use_case import (
    VoteForArticleUseCase
)


def test_post_article_vote_with_malformed_data_returns_bad_request(
    arf: APIRequestFactory,
    a_user_id: UserId,
    an_article_id: ArticleId
):
    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=VoteForArticleUseCaseNoopStub()
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'user_id': str(a_user_id),
                'article_id': str(an_article_id)
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == {
        'vote': [
            ErrorDetail("This field is required.", code='required')
        ]
    }


class VoteForArticleUseCaseNoopStub(VoteForArticleUseCase):
    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        raise Exception("This should never happen")
