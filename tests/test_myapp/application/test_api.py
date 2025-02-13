from http import HTTPStatus
from typing import Self
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from rest_framework.response import Response

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import VotingUserEntity
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.dependencies_container import build_production_dependencies_container

from rest_framework.test import APIRequestFactory


@pytest.fixture
def article_vote_view():
    dep_container = build_production_dependencies_container()
    return dep_container['article_vote_django_view']


def test_succeffully_vote_for_existing_article(
    arf: APIRequestFactory,
    article_vote_view,
):
    ArticleVoteEntity.save = MagicMock()
    VotingUserEntity.objects = VotingUserEntityObjectManagerMock(
        VotingUserEntity(
            user_id=UUID('9af8961e-0000-0000-0000-000000000000'),
            karma=10
        )
    )
    ArticleVoteEntity.objects = ArticleVoteEntityManagerMock(
        None
        # ArticleVoteEntity(
        #     id=UUID('10000000-0000-0000-0000-000000000000'),
        #     article_id=UUID('3f577757-0000-0000-0000-000000000000'),
        #     user_id=UUID('9af8961e-0000-0000-0000-000000000000'),
        #     vote=ArticleVoteEntity.VOTE_UP
        # )
    )

    response: Response = article_vote_view(
        arf.post(
            '/article_vote',
            {
                'article_id': ArticleId(UUID('3f577757-0000-0000-0000-000000000000')),
                'user_id': UserId(UUID('9af8961e-0000-0000-0000-000000000000')),
                'vote': Vote.DOWN.value
            },
            format='json'
        )
    )
    assert response.status_code == HTTPStatus.CREATED


class VotingUserEntityObjectManagerMock:
    stub: VotingUserEntity = None

    def __init__(self, stub: VotingUserEntity):
        self.stub = stub

    def get(self, *_args, **_kwargs) -> VotingUserEntity:
        return self.stub

    def filter(self, *_args, **_kwargs) -> Self:
        return self

    def first(self) -> VotingUserEntity:
        return self.stub


class ArticleVoteEntityManagerMock:
    stub: ArticleVoteEntity = None

    def __init__(self, stub: ArticleVoteEntity):
        self.stub = stub

    def get(self, *_args, **_kwargs) -> ArticleVoteEntity:
        return self.stub

    def filter(self, *_args, **_kwargs) -> Self:
        return self

    def first(self) -> ArticleVoteEntity:
        return self.stub
