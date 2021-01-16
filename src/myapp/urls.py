from typing import cast

from django.urls import path

from django.apps import apps as django_apps

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.apps import MyAppConfig

app_config: MyAppConfig = cast(MyAppConfig, django_apps.get_containing_app_config('myapp'))
article_vote_view = app_config.container['article_vote_view']

urlpatterns = [
    path('article_vote', article_vote_view)
]
