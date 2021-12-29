from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Event:
    id: UUID = field(init=False, kw_only=True)

