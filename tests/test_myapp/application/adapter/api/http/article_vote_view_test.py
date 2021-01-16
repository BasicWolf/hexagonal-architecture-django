from uuid import uuid4, UUID

from rest_framework import status
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    CastArticleVoteResult, VoteCastResult
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from tests.test_myapp.application.adapter.api.http.content_types import ContentType


def test_post_article_vote(arf: APIRequestFactory, user_id: UUID, article_id: UUID):
    cast_article_use_case_mock = CastArticleVoteUseCaseMock(
        returned_result=VoteCastResult(build_article_vote(
            user_id=user_id,
            article_id=article_id,
            vote=Vote.DOWN
        ))
    )

    article_vote_view = ArticleVoteView(cast_article_use_case_mock)
    response = article_vote_view.post(
        arf.post(
            f'/article_vote',
            data={
                'user_id': user_id, 
                'article_id': article_id,
                'vote': Vote.UP
            },
            content_type=ContentType.APPLICATION_JSON.value
        )
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == '{}'


def build_article_vote(
    user_id: UUID = uuid4(),
    article_id: UUID = uuid4(),
    vote: Vote = Vote.UP
) -> ArticleVote:
    return ArticleVote(
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
