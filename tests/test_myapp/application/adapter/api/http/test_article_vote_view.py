from http import HTTPStatus
from uuid import UUID, uuid4

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_for_article_result import (
    AlreadyVotedResult,
    InsufficientKarmaResult,
    SuccessfullyVotedResult,
    VoteForArticleResult
)
from myapp.application.ports.api.command.vote_for_article_command import (
    VoteForArticleCommand
)
from myapp.application.ports.api.vote_for_article_use_case import (
    VoteForArticleUseCase
)


def test_post_article_vote(
    arf: APIRequestFactory
):
    vote_for_article_use_case_mock = VoteForArticleUseCaseMock(
        returned_result=SuccessfullyVotedResult(
            user_id=UserId(UUID('9af8961e-0000-0000-0000-000000000000')),
            article_id=ArticleId(UUID('3f577757-0000-0000-0000-000000000000')),
            vote=Vote.DOWN
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=vote_for_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'user_id': UserId(UUID('9af8961e-0000-0000-0000-000000000000')),
                'article_id': ArticleId(UUID('3f577757-0000-0000-0000-000000000000')),
                'vote': Vote.DOWN.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.data == {
        'article_id': '3f577757-0000-0000-0000-000000000000',
        'user_id': '9af8961e-0000-0000-0000-000000000000',
        'vote': 'DOWN'
    }


def test_post_article_vote_with_malformed_data_returns_bad_request(
    arf: APIRequestFactory,
    user_id: UserId,
    article_id: ArticleId
):
    vote_for_article_use_case_mock = VoteForArticleUseCaseMock()

    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=vote_for_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'user_id': str(user_id),
                'article_id': str(article_id)
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_article_vote_with_insufficient_karma_returns_bad_request(
    arf: APIRequestFactory,
    article_id: ArticleId
):
    vote_for_article_use_case_mock = VoteForArticleUseCaseMock(
        returned_result=InsufficientKarmaResult(
            user_id=UserId(UUID('2e8a5b4e-0000-0000-0000-000000000000'))
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=vote_for_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'user_id': UserId(UUID('2e8a5b4e-0000-0000-0000-000000000000')),
                'article_id': article_id,
                'vote': Vote.UP.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == {
        'status': 400,
        'detail': "User 2e8a5b4e-0000-0000-0000-000000000000 does not have enough "
                  "karma to vote for an article",
        'title': "Cannot vote for an article"
    }


def test_post_article_vote_with_same_user_and_article_id_twice_returns_conflict(
    arf: APIRequestFactory
):
    vote_for_article_use_case_mock = VoteForArticleUseCaseMock(
        returned_result=AlreadyVotedResult(
            user_id=UserId(UUID('a3854820-0000-0000-0000-000000000000')),
            article_id=ArticleId(UUID('dd494bd6-0000-0000-0000-000000000000'))
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        vote_for_article_use_case=vote_for_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'user_id': UserId(UUID('a3854820-0000-0000-0000-000000000000')),
                'article_id': ArticleId(UUID('dd494bd6-0000-0000-0000-000000000000')),
                'vote': Vote.UP.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.data == {
        'status': 409,
        'detail': "User \"a3854820-0000-0000-0000-000000000000\" has already voted"
                  " for article \"dd494bd6-0000-0000-0000-000000000000\"",
        'title': "Cannot vote for an article"
    }


class VoteForArticleUseCaseMock(VoteForArticleUseCase):
    called_with_command = None

    def __init__(
        self,
        returned_result: VoteForArticleResult = None
    ):
        if returned_result is None:
            returned_result = SuccessfullyVotedResult(
                user_id=UserId(uuid4()),
                article_id=ArticleId(uuid4()),
                vote=Vote.UP
            )
        self._returned_result = returned_result

    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        self.called_with_command = command
        return self._returned_result
