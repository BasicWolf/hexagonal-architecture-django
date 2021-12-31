from dataclasses import dataclass

import pytest

from myapp.eventlib.event import Event
from myapp.eventlib.event_dispatcher import EventDispatcher


@pytest.fixture
def event_dispatcher() -> EventDispatcher:
    return EventDispatcher()


@dataclass
class SampleEvent(Event):
    samples: int = 0


def test_register_event_handler(event_dispatcher: EventDispatcher):
    def sample_event_handler(sample_event: SampleEvent):
        pass

    event_dispatcher.register_handler(SampleEvent, sample_event_handler)

    assert event_dispatcher.get_handlers_for(SampleEvent) == [sample_event_handler]


def test_handle_dispatched_event(
    event_dispatcher: EventDispatcher
):
    handled_samples = 0

    def sample_event_handler(sample_event: SampleEvent):
        nonlocal handled_samples
        handled_samples = sample_event.samples

    event_dispatcher.register_handler(SampleEvent, sample_event_handler)
    event_dispatcher.dispatch(SampleEvent(samples=100))

    assert handled_samples == 100


def test_handle_dispatched_event_by_two_handlers(
    event_dispatcher: EventDispatcher
):
    class SampleEventHandler:
        handled_samples = 0

        def __call__(self, sample_event: SampleEvent):
            self.handled_samples = sample_event.samples

    first_handler = SampleEventHandler()
    second_handler = SampleEventHandler()
    event_dispatcher.register_handler(SampleEvent, first_handler)
    event_dispatcher.register_handler(SampleEvent, second_handler)
    event_dispatcher.dispatch(SampleEvent(samples=37))

    assert first_handler.handled_samples == 37
    assert second_handler.handled_samples == 37
