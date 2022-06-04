from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_voting_user_not_found_is_bad_request(client, a_user_id, an_article_id):
    response = client.post('/api/article_vote', {
        'user_id': a_user_id,
        'article_id': an_article_id,
        'vote': 'UP'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
