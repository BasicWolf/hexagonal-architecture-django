from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_voting_for_non_existing_user_returns_response_with_status_not_found(
    client, a_user_id, an_article_id
):
    response = client.post('/api/article_vote', {
        'user_id': a_user_id,
        'article_id': an_article_id,
        'vote': 'UP'
    })
    assert response.status_code == HTTPStatus.NOT_FOUND
