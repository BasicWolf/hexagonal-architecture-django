from uuid import uuid4

from django.db import models


class ArticleVote(models.Model):
    VOTE_UP = 1
    VOTE_DOWN = 2

    VOTES_CHOICES = [
        (VOTE_UP, 'UP'),
        (VOTE_DOWN, 'DOWN')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    post_id = models.UUIDField()
    vote = models.IntegerField(choices=VOTES_CHOICES)

    class Meta:
        unique_together = [['user_id', 'post_id']]

