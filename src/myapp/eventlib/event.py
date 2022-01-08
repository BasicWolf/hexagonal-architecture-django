from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Event:
    id: UUID = field(kw_only=True, default_factory=uuid4, compare=False)
