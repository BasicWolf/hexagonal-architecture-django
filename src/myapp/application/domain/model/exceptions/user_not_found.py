from uuid import UUID

from myapp.application.domain.model.exceptions.entity_not_found import EntityNotFound


class UserNotFound(EntityNotFound):
    def __init__(self, user_id: UUID):
        super().__init__(user_id, f"User '{user_id}' not found")

