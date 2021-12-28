from typing import Callable, Dict, List, Type, TypeVar

from myapp.eventlib.event import Event

T_contra = TypeVar('T_contra', bound=Event, covariant=True)
EventHandlerBaseType = Callable[[T_contra], None]


class EventDispatcher:
    handlers: Dict[Type[Event], List[EventHandlerBaseType]] = {}

    def register_handler(
        self,
        event_type: Type[T_contra],
        event_handler: Callable[[T_contra], None]
    ):
        self.handlers.setdefault(event_type, list())
        self.handlers[event_type].append(event_handler)

    def dispatch(self, event: Event):
        event_handlers = self.handlers.get(type(event), list())
        for event_handler in event_handlers:
            event_handler(event)
