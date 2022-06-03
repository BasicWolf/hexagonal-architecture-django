from __future__ import annotations

from uuid import uuid4

from django.db import models


class VotingUserEntity(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    class Meta:
        # in a real application this could be a view or a table intended for reads only
        # (i.e. think of CQRS).
        db_table = 'voting_user'
