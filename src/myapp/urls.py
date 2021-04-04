from typing import cast

from django.apps import apps as django_apps
from django.urls import path

from myapp.apps import MyAppConfig

app_config: MyAppConfig = cast(MyAppConfig, django_apps.get_containing_app_config('myapp'))
article_vote_django_view = app_config.container['article_vote_django_view']

urlpatterns = [
    path('article_vote', article_vote_django_view)
]
