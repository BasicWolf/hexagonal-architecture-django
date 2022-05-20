from typing import Any, Dict

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.service.article_rating_service import ArticleRatingService


def build_production_dependencies_container() -> Dict[str, Any]:
    voting_user_repository = VotingUserRepository()
    article_vote_repository = ArticleVoteRepository()

    article_rating_service = ArticleRatingService(
        find_voting_user_port=voting_user_repository,
        save_article_vote_port=article_vote_repository,
    )

    article_vote_django_view = ArticleVoteView.as_view(
        vote_for_article_use_case=article_rating_service
    )

    return {
        'article_vote_django_view': article_vote_django_view
    }
