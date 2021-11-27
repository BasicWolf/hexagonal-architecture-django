from __future__ import annotations

from uuid import uuid4

from django.db import models

from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import ArticleVote


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

    @classmethod
    def from_article_vote(cls, article_vote: ArticleVote) -> ArticleVoteEntity:
        return ArticleVoteEntity(
            article_id=article_vote.article_id,
            user_id=article_vote.user_id,
            vote=article_vote.vote.value
        )

    def to_article_vote(self) -> ArticleVote:
        return ArticleVote(
            user_id=UserId(self.user_id),
            article_id=ArticleId(self.article_id),
            vote=Vote(self.vote)
        )
