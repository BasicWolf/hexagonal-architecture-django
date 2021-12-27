from dataclasses import dataclass

from myapp.eventlib.event import Event
from myapp.eventlib.event_dispatcher import EventDispatcher


def test_register_event_handler(event_dispatcher: EventDispatcher):
    @dataclass
    class SampleEvent(Event):
        samples: int = 0

    def sample_event_handler(sample_event: SampleEvent):
        pass

    event_dispatcher.register_handler(SampleEvent, sample_event_handler)

    assert event_dispatcher.handlers[SampleEvent] == [sample_event_handler]


def test_dispatched_event_gets_handled(
    event_dispatcher: EventDispatcher
):
    @dataclass
    class SampleEvent(Event):
        samples: int = 0

    handled_samples = 0

    def sample_event_handler(sample_event: SampleEvent):
        nonlocal handled_samples
        handled_samples = sample_event.samples

    event_dispatcher.register_handler(SampleEvent, sample_event_handler)
    event_dispatcher.dispatch(SampleEvent(samples=100))

    assert handled_samples == 100
