from uuid import UUID, uuid4

import pytest
from rest_framework.test import APIRequestFactory

from myapp.application.domain.model.identifier.user_id import UserId


@pytest.fixture
def article_id() -> UUID:
    return uuid4()


@pytest.fixture
def user_id() -> UserId:
    return UserId(uuid4())


@pytest.fixture
def article_vote_id() -> UUID:
    return uuid4()


@pytest.fixture
def arf():
    return APIRequestFactory()
