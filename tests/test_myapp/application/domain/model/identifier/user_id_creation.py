from uuid import UUID, uuid4

from myapp.application.domain.model.identifier.user_id import UserId


def create_user_id(*args, **kwargs):
    if args or kwargs:
        return UserId(UUID(*args, **kwargs))
    else:
        return UserId(uuid4())
