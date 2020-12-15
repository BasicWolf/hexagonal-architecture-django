from uuid import UUID

import pytest
from django.db import transaction, IntegrityError

from myapp.application.adapter.spi.persistence.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote


@transaction.atomic
def hoho():
    article_vote_repository = ArticleVoteRepository()

    print('11111111111111111111111111')
    article_vote_repository.save_article_vote(
        ArticleVote(
            user_id=UUID('76bc279b-883f-4809-a030-e069d3517b5c'),
            post_id=UUID('e55e700e-9fae-4954-872a-675757112fdc'),
            vote=Vote.UP
        )
    )
    print('22222222222222222222222222222')
    try:
        article_vote_repository.save_article_vote(
            ArticleVote(
                user_id=UUID('76bc279b-883f-4809-a030-e069d3517b5c'),
                post_id=UUID('e55e700e-9fae-4954-872a-675757112fdc'),
                vote=Vote.UP
            )
        )
    except IntegrityError:
        return 10

    print('3333333333333333333333333333333')
    article_vote_repository.save_article_vote(
        ArticleVote(
            user_id=UUID('76bc279b-883f-4809-a030-e069d3517b5c'),
            post_id=UUID('e55e700e-9fae-4954-872a-675757112fdc'),
            vote=Vote.UP
        )
    )
    print('44444444444444444444444444444444')

@pytest.mark.django_db
def test_save_article_vote():
    assert hoho() == 10


