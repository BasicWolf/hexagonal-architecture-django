from http import HTTPStatus
from uuid import uuid4, UUID

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import CastArticleVoteResult, \
    VoteAlreadyCast, InsufficientKarma
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from tests.test_myapp.application.domain.model.voting_user import createUserId, \
    createArticleId


def test_post_article_vote(
    arf: APIRequestFactory,
    article_vote_id: UUID,
    user_id: UserId,
    article_id: ArticleId
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=ArticleVote(
            id=article_vote_id,
            user_id=user_id,
            article_id=article_id,
            vote=Vote.DOWN
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=cast_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            f'/article_vote',
            {
                'user_id': user_id,
                'article_id': article_id,
                'vote': Vote.DOWN.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.data == {
        'id': str(article_vote_id),
        'article_id': str(article_id),
        'user_id': str(user_id),
        'vote': 'DOWN'
    }


def test_post_article_vote_with_malformed_data_returns_bad_request(
    arf: APIRequestFactory
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock()

    article_vote_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=cast_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            f'/article_vote',
            {
                'user_id': str(uuid4()),
                'article_id': str(uuid4())
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_article_vote_with_insufficient_karma_returns_bad_request(
    arf: APIRequestFactory,
    user_id: UserId,
    article_id: UUID
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=InsufficientKarma(
            user_id=user_id
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=cast_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            f'/article_vote',
            {
                'user_id': user_id,
                'article_id': article_id,
                'vote': Vote.UP.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == {
        'status': 400,
        'detail': f"User {user_id} does not have enough karma to cast a vote",
        'title': "Cannot cast a vote"
    }


def test_post_article_vote_with_same_user_and_article_id_twice_returns_conflict(
    arf: APIRequestFactory,
    user_id: UserId,
    article_id: UUID
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=VoteAlreadyCast(
            user_id=user_id,
            article_id=article_id
        )
    )

    article_vote_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=cast_article_use_case_mock
    )

    response: Response = article_vote_view(
        arf.post(
            f'/article_vote',
            {
                'user_id': user_id,
                'article_id': article_id,
                'vote': Vote.UP.value
            },
            format='json'
        )
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.data == {
        'status': 409,
        'detail': f"User \"{user_id}\" has already cast a vote for article \"{article_id}\"",
        'title': "Cannot cast a vote"
    }


def build_article_vote(
    id: UUID = None,
    user_id: UserId = None,
    article_id: ArticleId = None,
    vote: Vote = Vote.UP
) -> ArticleVote:
    id = id or uuid4()
    user_id = user_id or createUserId()
    article_id = article_id or createArticleId()

    return ArticleVote(
        id=id,
        user_id=user_id,
        article_id=article_id,
        vote=vote
    )


class CastArticleVoteUseCaseMock(CastArticleVoteUseCase):
    called_with_command = None

    def __init__(
        self,
        returned_result: CastArticleVoteResult = build_article_vote()
    ):
        self._returned_result = returned_result

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        self.called_with_command = command
        return self._returned_result
