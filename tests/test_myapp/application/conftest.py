from uuid import UUID, uuid4

import pytest


@pytest.fixture
def article_id() -> UUID:
    return uuid4()


@pytest.fixture
def user_id() -> UUID:
    return uuid4()
