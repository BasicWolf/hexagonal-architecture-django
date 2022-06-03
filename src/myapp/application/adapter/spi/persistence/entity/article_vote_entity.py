from __future__ import annotations

from uuid import uuid4

from django.db import models


class ArticleVoteEntity(models.Model):
    # the `up` and `down` values are chosen to simplify mapping to/from domain model
    # for real applications integer fields might be more suitable.
    VOTE_UP = 'up'
    VOTE_DOWN = 'down'

    VOTES_CHOICES = [
        (VOTE_UP, 'UP'),
        (VOTE_DOWN, 'DOWN')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    article_id = models.UUIDField()
    vote = models.CharField(max_length=4, choices=VOTES_CHOICES)

    class Meta:
        unique_together = [['user_id', 'article_id']]
        db_table = 'article_vote'
