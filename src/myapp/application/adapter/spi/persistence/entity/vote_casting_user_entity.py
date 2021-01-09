from uuid import uuid4

from django.db import models

from myapp.application.domain.model.vote_casting_user import VoteCastingUser


class VoteCastingUserEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    class Meta:
        db_table = 'user_data'

    def to_domain_model(self) -> VoteCastingUser:
        return VoteCastingUser(self.id, self.karma)

