from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Event:
    id: UUID = field(default_factory=uuid4)
