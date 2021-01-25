from http import HTTPStatus
from uuid import uuid4, UUID

import pytest
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    CastArticleVoteResult, VoteCastResult, InsufficientKarmaResult, VoteAlreadyCastResult
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase


@pytest.fixture
def article_vote_id() -> UUID:
    return uuid4()


def test_post_article_vote(
    arf: APIRequestFactory,
    article_vote_id: UUID,
    user_id: UUID,
    article_id: UUID
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=VoteCastResult(build_article_vote(
            id=article_vote_id,
            user_id=user_id,
            article_id=article_id,
            vote=Vote.DOWN
        ))
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


def test_post_article_vote_with_insufficient_karma_returns_bad_request(
    arf: APIRequestFactory,
    user_id: UUID,
    article_id: UUID
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=InsufficientKarmaResult(
            user_with_insufficient_karma_id=user_id
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


def test_post_article_vote_returns_conflict(
    arf: APIRequestFactory,
    user_id: UUID,
    article_id: UUID
):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=VoteAlreadyCastResult(
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


def build_article_vote(
    id: UUID = uuid4(),
    user_id: UUID = uuid4(),
    article_id: UUID = uuid4(),
    vote: Vote = Vote.UP
) -> ArticleVote:
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
        returned_result: CastArticleVoteResult = VoteCastResult(build_article_vote())
    ):
        self._returned_result = returned_result

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        self.called_with_command = command
        return self._returned_result
