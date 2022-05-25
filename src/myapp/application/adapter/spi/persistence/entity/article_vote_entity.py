from __future__ import annotations

from uuid import uuid4

from django.db import models

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import ArticleVote


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

    @classmethod
    def from_domain_model(cls, article_vote: ArticleVote) -> ArticleVoteEntity:
        return ArticleVoteEntity(
            article_id=article_vote.article_id,
            user_id=article_vote.user_id,
            vote=article_vote.vote.value
        )

    def to_domain_model(self) -> ArticleVote:
        return ArticleVote(
            ArticleId(self.article_id),
            UserId(self.user_id),
            Vote(self.vote)
        )
