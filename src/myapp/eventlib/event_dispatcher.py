from typing import Callable, cast, Dict, List, Type, TypeVar

from myapp.eventlib.event import Event

T = TypeVar('T', bound=Event)
EventHandlerBaseType = Callable[[Event], None]


class EventDispatcher:
    handlers: Dict[Type[Event], List[EventHandlerBaseType]] = {}

    def register_handler(
        self,
        event_type: Type[T],
        event_handler: Callable[[T], None]
    ):
        self.handlers.setdefault(event_type, list())
        self.handlers[event_type].append(
            cast(EventHandlerBaseType, event_handler)  # use cast to work around mypy bug?
        )

    def dispatch(self, event: T):
        event_handlers = self.handlers.get(type(event), [])
        for event_handler in event_handlers:
            event_handler(event)
