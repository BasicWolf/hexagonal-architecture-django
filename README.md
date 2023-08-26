# hexagonal-architecture-django
Experiments with Django and Hexagonal Architecture

## Project pulse

I started this project to research building Django apps
following the Hexagonal Architecture and Domain-Driven Design (DDD) principles.
The code has been through numerous iterations and incarnations, as my understanding of 
the topics. It took me two and a half years to conclude the project and put down my 
experience in a series of articles.

While the project currently resides in a maintenance state, it's worth noting that 
all dependencies continue to be updated automatically via 
[Mend Renovate](https://www.mend.io/renovate/) (bless you, people!)
Moreover, the presence of an extensive test suite diligently ensures 
its ongoing relevance and accuracy.

### Articles

* [Hexagonal architecture of ports and adapters, Dependency injection and Python - Part I](https://znasibov.info/posts/2021/10/30/hexarch_di_python_part_1.html)
* [Hexagonal architecture and Python - Part II: Domain, Application Services, Ports and Adapters](https://znasibov.info/posts/2022/09/18/hexarch_di_python_part_2.html)
* [Hexagonal architecture and Python - Part III: Persistence, Transactions, Exceptions and The Final Assembly](https://znasibov.info/posts/2022/12/31/hexarch_di_python_part_3.html)

Originally, this project was a supporting example for
[Domain-driven design, Hexagonal architecture of ports and adapters, Dependency injection и Python](https://habr.com/ru/post/559560/)
article.
The article was written in Russian language and was published on 31 May 2021
at russian tech-blog platform [Habr](https://habr.com/).
This code is now tagged as ["habr"](https://github.com/BasicWolf/hexagonal-architecture-django/tree/habr).

## Finding your way around

**Installation**

Requires ``Python 3.10`` or later. CI runs on Python ``3.11``.

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
export DJANGO_SETTINGS_MODULE="hexarch_project.test_settings"
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
curl http://localhost:8000/api/article_vote \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
      "user_id": "e47cec00-c22a-486d-afe6-e76902f211c1", 
      "article_id": "60ccea0c-0bf2-4726-8ac7-324fa03a74cd",
      "vote": "UP"
  }'
```

Non-existing user:
```shell
curl http://localhost:8000/api/article_vote \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
      "user_id": "efed6f83-49ee-4cbc-bdbd-2b92bf428f2b", 
      "article_id": "60ccea0c-0bf2-4726-8ac7-324fa03a74cd",
      "vote": "UP"
  }' 
```
