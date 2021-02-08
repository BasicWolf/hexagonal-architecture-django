from uuid import uuid4

from django.db import models

from myapp.application.domain.model.voting_user import VotingUser


class VoteCastingUserEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    class Meta:
        db_table = 'user_data'

    def to_domain_model(self) -> VotingUser:
        return VotingUser(self.id, self.karma)

