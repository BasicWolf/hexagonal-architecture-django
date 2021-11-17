# hexagonal-architecture-django
Experiments with Django and Hexagonal Architecture



This project was originally a supporting example for
[Domain-driven design, Hexagonal architecture of ports and adapters, Dependency injection и Python](https://habr.com/ru/post/559560/)
article.
The article was written in Russian language and was published on 31 May 2021
at russian tech-blog platform [Habr](https://habr.com/).
This code is now tagged as ["habr"](https://github.com/BasicWolf/hexagonal-architecture-django/tree/habr).


**Installation**

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

**Static type checks (mypy)**

```shell
export MYPYPATH=src/
mypy --namespace-packages -v -p myapp
```

**Run unit tests**

```shell
export PYTHONPATH=${PYTHONPATH}:./:src/
pytest
```

**Run application**

```shell
./src/manage.py migrate
./src/manage.py runserver
```

**Test with cURL**

With existing user:
```shell
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id": "e47cec00-c22a-486d-afe6-e76902f211c1", "article_id":
  "60ccea0c-0bf2-4726-8ac7-324fa03a74cd", "vote": "UP"}' \
  http://localhost:8000/api/article_vote
```

Non-existing user:
```shell
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id": "efed6f83-49ee-4cbc-bdbd-2b92bf428f2b", "article_id":
  "60ccea0c-0bf2-4726-8ac7-324fa03a74cd", "vote": "UP"}' \
  http://localhost:8000/api/article_vote
```
