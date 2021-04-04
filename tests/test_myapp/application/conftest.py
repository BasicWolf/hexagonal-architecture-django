from uuid import UUID, uuid4

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def article_id() -> UUID:
    return uuid4()


@pytest.fixture
def user_id() -> UUID:
    return uuid4()


@pytest.fixture
def article_vote_id() -> UUID:
    return uuid4()


@pytest.fixture
def arf():
    return APIRequestFactory()
