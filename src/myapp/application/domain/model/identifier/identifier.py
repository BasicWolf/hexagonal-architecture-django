from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Identifier:
    id: UUID = field(default_factory=uuid4)
