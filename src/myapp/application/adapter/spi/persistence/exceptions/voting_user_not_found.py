from myapp.application.adapter.spi.persistence.exceptions.entity_not_found import \
    EntityNotFound
from myapp.application.domain.model.identifier.user_id import UserId


class VotingUserNotFound(EntityNotFound):
    def __init__(self, user_id: UserId):
        super().__init__(user_id, f"User '{user_id}' not found")
