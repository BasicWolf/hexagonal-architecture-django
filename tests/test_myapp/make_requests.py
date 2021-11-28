import requests

response = requests.post('http://localhost:8000/article_vote', json={
    'id': 1,
    'name': 'Jessa'
})
print(response.content)
