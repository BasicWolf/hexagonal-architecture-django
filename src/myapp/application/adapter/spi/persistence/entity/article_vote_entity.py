from __future__ import annotations

from uuid import uuid4

from django.db import models

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote


class ArticleVoteEntity(models.Model):
    VOTE_UP = 1
    VOTE_DOWN = 2

    VOTES_CHOICES = [
        (VOTE_UP, 'UP'),
        (VOTE_DOWN, 'DOWN')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    article_id = models.UUIDField()
    vote = models.IntegerField(choices=VOTES_CHOICES)

    class Meta:
        unique_together = [['user_id', 'article_id']]
        db_table = 'article_vote'

    @classmethod
    def from_domain_model(cls, article_vote: ArticleVote) -> ArticleVoteEntity:
        vote: int = {
            Vote.UP: cls.VOTE_UP,
            Vote.DOWN: cls.VOTE_DOWN
        }[article_vote.vote]

        return ArticleVoteEntity(
            id=article_vote.id,
            article_id=article_vote.article_id,
            user_id=article_vote.user_id,
            vote=vote
        )

    def to_domain_model(self) -> ArticleVote:
        vote: Vote = {
            self.VOTE_UP: Vote.UP,
            self.VOTE_DOWN: Vote.DOWN
        }[self.vote]

        return ArticleVote(
            id=self.id,
            user_id=UserId(self.user_id),
            article_id=self.article_id,
            vote=vote
        )
