from uuid import UUID

import pytest
from django.db import IntegrityError

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote


@pytest.mark.django_db
def test_save_article_vote(user_id: UUID, article_id: UUID):
    article_vote_repository = ArticleVoteRepository()

    article_vote_repository.save_article_vote(
        ArticleVote(
            user_id=user_id,
            article_id=article_id,
            vote=Vote.UP
        )
    )

    assert ArticleVoteEntity.objects.filter(
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_UP
    ).exists()


@pytest.mark.django_db
def test_saving_identical_article_votes_raises_integrity_error(
    user_id: UUID, article_id: UUID
):
    article_vote_repository = ArticleVoteRepository()

    article_vote = ArticleVote(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )

    article_vote_repository.save_article_vote(article_vote)

    with pytest.raises(IntegrityError) as exception_info:
        article_vote_repository.save_article_vote(article_vote)
    exception_info.match('UNIQUE constraint failed: article_vote.user_id, '
                         'article_vote.article_id')
