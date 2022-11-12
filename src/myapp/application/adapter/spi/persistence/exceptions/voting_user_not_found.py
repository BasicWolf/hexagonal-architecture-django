from myapp.application.domain.model.identifier.user_id import UserId


class VotingUserNotFound(RuntimeError):
    def __init__(self, user_id: UserId):
        super().__init__(f"User '{user_id}' not found")
