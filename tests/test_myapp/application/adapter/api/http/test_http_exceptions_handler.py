from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_voting_user_not_found_is_bad_request(client, user_id, article_id):
    response = client.post('/api/article_vote', {
        'user_id': user_id,
        'article_id': article_id,
        'vote': 'UP'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
