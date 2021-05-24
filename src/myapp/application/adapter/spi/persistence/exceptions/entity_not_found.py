from typing import Optional
from uuid import UUID


class EntityNotFound(RuntimeError):
    """Base class for queried entities not being found"""
    entity_id: UUID

    def __init__(self, entity_id: UUID, message: Optional[str] = None):
        self.entity_id = entity_id
        if message is None:
            message = f"Entity '{entity_id}' not found"
        super().__init__(message)

