from typing import List

from myapp.eventlib.event import Event
from myapp.eventlib.event_dispatcher import EventDispatcher


class InterceptingEventDispatcher(EventDispatcher):
    dispatched_events: List[Event] = []

    def dispatch(self, event: Event):
        super().dispatch(event)
        self.dispatched_events.append(event)

    def check_event_dispatched(self, event: Event) -> bool:
        return event in self.dispatched_events
