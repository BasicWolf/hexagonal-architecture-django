from typing import Any, Dict

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.service.post_rating_service import PostRatingService


def build_production_dependencies_container() -> Dict[str, Any]:
    voting_user_repository = VotingUserRepository()
    article_vote_repository = ArticleVoteRepository()

    get_vote_casting_user_adapter = voting_user_repository

    cast_article_vote_use_case = PostRatingService(
        article_vote_repository,
        get_vote_casting_user_adapter,
        article_vote_repository
    )

    article_vote_django_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=cast_article_vote_use_case
    )

    return {
        'article_vote_django_view': article_vote_django_view
    }
