from uuid import uuid4

from django.db import models


class VotingUserEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    class Meta:
        # in real application this should rather be a view
        db_table = 'user_data'
