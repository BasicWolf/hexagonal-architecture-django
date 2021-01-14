from django.urls import path

from django.apps import apps as django_apps

from myapp import views
from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.apps import MyAppConfig

app_config: MyAppConfig = django_apps.get_containing_app_config('myapp')
article_vote_view: ArticleVoteView = app_config.container['article_vote_view']

urlpatterns = [
    path('', views.index, name='index'),
    path('article_vote', article_vote_view)
]
