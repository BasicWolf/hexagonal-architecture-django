from uuid import UUID

from myapp.application.adapter.spi.persistence.exceptions.entity_not_found import EntityNotFound


class VotingUserNotFound(EntityNotFound):
    def __init__(self, user_id: UUID):
        super().__init__(user_id, f"User '{user_id}' not found")

