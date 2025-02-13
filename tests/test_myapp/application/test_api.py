from http import HTTPStatus
from typing import Optional, Self
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import VotingUserEntity
from myapp.dependencies_container import build_production_dependencies_container


def test_successfully_vote_for_existing_article(
    given_voting_user,
    given_no_existing_article_votes,
    mock_persisting_article_vote,
    post_article_vote
):
    given_voting_user(
        user_id=UUID('9af8961e-0000-0000-0000-000000000000'),
        karma=10
    )
    given_no_existing_article_votes()
    mock_persisting_article_vote()

    response: Response = post_article_vote(
        article_id='3f577757-0000-0000-0000-000000000000',
        user_id='9af8961e-0000-0000-0000-000000000000',
        vote='DOWN'
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.data == {
        'article_id': '3f577757-0000-0000-0000-000000000000',
        'user_id': '9af8961e-0000-0000-0000-000000000000',
        'vote': 'DOWN'
    }


@pytest.fixture
def given_voting_user():
    original_voting_user_entity_manager = VotingUserEntity.objects

    def _given_voting_user(user_id: UUID, karma: int):
        VotingUserEntity.objects = VotingUserEntityObjectManagerMock(
            VotingUserEntity(
                user_id=user_id,
                karma=karma
            )
        )  # type: ignore
    yield _given_voting_user

    VotingUserEntity.objects = original_voting_user_entity_manager


@pytest.fixture
def given_no_existing_article_votes():
    original_article_vote_entity_manager = ArticleVoteEntity.objects

    def _given_no_existing_article_votes():
        ArticleVoteEntity.objects = ArticleVoteEntityManagerMock(None)  # type: ignore
    yield _given_no_existing_article_votes

    ArticleVoteEntity.objects = original_article_vote_entity_manager


@pytest.fixture
def mock_persisting_article_vote():
    original_article_vote_entity_save = ArticleVoteEntity.save

    def _mock_persisting_article_vote():
        ArticleVoteEntity.save = MagicMock()  # type: ignore[method-assign]
    yield _mock_persisting_article_vote

    ArticleVoteEntity.save = original_article_vote_entity_save  # type: ignore[method-assign]


@pytest.fixture
def post_article_vote(article_vote_view):
    def _post_article_vote(article_id: str, user_id: str, vote: str) -> Response:
        return article_vote_view(
            APIRequestFactory().post(
                '/article_vote',
                {
                    'article_id': article_id,
                    'user_id': user_id,
                    'vote': vote
                },
                format='json'
            )
        )
    return _post_article_vote


@pytest.fixture
def article_vote_view(production_dependencies_container):
    return production_dependencies_container['article_vote_django_view']


@pytest.fixture(scope='module')
def production_dependencies_container():
    return build_production_dependencies_container()


class VotingUserEntityObjectManagerMock:
    stub: VotingUserEntity | None = None

    def __init__(self, stub: VotingUserEntity):
        super().__init__()
        self.stub = stub

    def get(self, *_args, **_kwargs) -> VotingUserEntity:
        if self.stub is None:
            raise VotingUserEntity.DoesNotExist()
        return self.stub

    def filter(self, *_args, **_kwargs) -> Self:
        return self

    def first(self) -> VotingUserEntity | None:
        return self.stub


class ArticleVoteEntityManagerMock:
    stub: Optional[ArticleVoteEntity] = None

    def __init__(self, stub: Optional[ArticleVoteEntity]):
        super().__init__()
        self.stub = stub

    def get(self, *_args, **_kwargs) -> ArticleVoteEntity:
        if self.stub is None:
            raise ArticleVoteEntity.DoesNotExist()
        return self.stub

    def filter(self, *_args, **_kwargs) -> Self:
        return self

    def first(self) -> ArticleVoteEntity | None:
        return self.stub
