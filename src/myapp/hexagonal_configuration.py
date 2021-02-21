from typing import Dict, Any

from myapp.application.adapter.api.http.article_vote_view import ArticleVoteView
from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.adapter.spi.persistence.repository.voting_user_repository import \
    VotingUserRepository
from myapp.application.service.post_rating_service import PostRatingService


def build_production_ioc_container() -> Dict[str, Any]:
    _article_vote_repository = ArticleVoteRepository()
    article_vote_exists_adapter = _article_vote_repository
    save_article_vote_adapter = _article_vote_repository

    get_vote_casting_user_adapter = VotingUserRepository()

    _cast_article_vote_use_case = PostRatingService(
        article_vote_exists_adapter,
        get_vote_casting_user_adapter,
        save_article_vote_adapter
    )

    article_vote_view = ArticleVoteView.as_view(
        cast_article_vote_use_case=_cast_article_vote_use_case
    )

    return {
        'article_vote_view': article_vote_view
    }

