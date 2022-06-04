import random
from uuid import uuid4

import pytest
from rest_framework.test import APIRequestFactory

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


@pytest.fixture
def an_article_id() -> ArticleId:
    return ArticleId(uuid4())


@pytest.fixture
def a_user_id() -> UserId:
    return UserId(uuid4())


@pytest.fixture
def a_vote() -> Vote:
    return random.choice(list(Vote))


@pytest.fixture
def arf():
    return APIRequestFactory()
