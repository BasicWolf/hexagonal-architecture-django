from __future__ import annotations

from uuid import uuid4

from django.db import models

from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


class VotingUserEntity(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    voted: bool = False

    class Meta:
        # in a real application this could be a view or a table intended for reads only
        # (i.e. think of CQRS).
        db_table = 'voting_user'

    @classmethod
    def create(cls, *args, voted: bool = False, **kwargs) -> VotingUserEntity:
        entity = cls(*args, **kwargs)  # type: ignore
        entity.voted = voted
        return entity

    def to_domain_model(self) -> VotingUser:
        return VotingUser(
            UserId(self.user_id),
            Karma(self.karma),
            self.voted
        )
