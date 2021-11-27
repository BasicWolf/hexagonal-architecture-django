from __future__ import annotations

from uuid import uuid4

from django.db import models

from myapp.application.domain.model.vote import Vote


class ArticleVoteEntity(models.Model):
    VOTE_UP = Vote.UP.value
    VOTE_DOWN = Vote.DOWN.value

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
