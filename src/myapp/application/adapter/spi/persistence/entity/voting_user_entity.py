from typing import Optional
from uuid import uuid4

from django.db import models

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.voting_user import VotingUser


class VotingUserEntity(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    karma = models.IntegerField()

    class Meta:
        # in real application this should rather be a view
        db_table = 'user_data'

    def to_domain_model(self, article_vote: Optional[ArticleVote]):
        if (article_vote is not None
            and article_vote.user_id != UserId(self.user_id)):
            raise ValueError("Invalid State: Article Vote does not belong to the user")

        return VotingUser(
            UserId(self.user_id),
            Karma(self.karma),
            article_vote
        )
