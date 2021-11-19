from uuid import uuid4

from myapp.application.domain.model.identifier.user_id import UserId


def create_user_id():
    return UserId(uuid4())
