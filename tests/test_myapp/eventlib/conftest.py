import pytest

from myapp.eventlib.event_dispatcher import EventDispatcher


@pytest.fixture
def event_dispatcher() -> EventDispatcher:
    return EventDispatcher()
