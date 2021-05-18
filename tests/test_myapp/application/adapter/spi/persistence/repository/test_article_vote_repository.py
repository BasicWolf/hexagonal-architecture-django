from uuid import UUID

import pytest
from django.db import IntegrityError

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote


@pytest.mark.integration
@pytest.mark.django_db
def test_save_article_vote_persists_to_database(
    article_vote_id: UUID,
    user_id: UUID,
    article_id: UUID
):
    article_vote_repository = ArticleVoteRepository()

    article_vote_repository.save_article_vote(
        ArticleVote(
            id=article_vote_id,
            user_id=user_id,
            article_id=article_id,
            vote=Vote.UP
        )
    )

    assert ArticleVoteEntity.objects.filter(
        id=article_vote_id,
        user_id=user_id,
        article_id=article_id,
        vote=ArticleVoteEntity.VOTE_UP
    ).exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_save_article_vote_returns_article_vote(
    article_vote_id: UUID,
    user_id: UUID,
    article_id: UUID
):
    article_vote_repository = ArticleVoteRepository()

    unsaved_article_vote = ArticleVote(
        id=article_vote_id,
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )
    saved_article_vote = article_vote_repository.save_article_vote(unsaved_article_vote)

    assert saved_article_vote == unsaved_article_vote
    assert saved_article_vote is not unsaved_article_vote


@pytest.mark.integration
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
