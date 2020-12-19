from uuid import UUID, uuid4

import pytest
from django.db import connection, IntegrityError

from myapp.application.adapter.spi.persistence.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.adapter.spi.persistence.entity.article_vote import \
    ArticleVoteEntity
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from tests.myapp.application.adapter.spi.persistence.namedtuple_fetchall import \
    namedtuple_fetchall


@pytest.fixture
def article_id() -> UUID:
    return uuid4()


@pytest.fixture
def user_id() -> UUID:
    return uuid4()


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

    with connection.cursor() as cursor:
        cursor.execute(f'SELECT user_id, article_id, vote from '
                       f'{ArticleVoteEntity._meta.db_table}')
        aritcle_vote_row = namedtuple_fetchall(cursor)[0]

        assert user_id == UUID(aritcle_vote_row.user_id)
        assert article_id == UUID(aritcle_vote_row.article_id)
        assert 1 == aritcle_vote_row.vote


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
