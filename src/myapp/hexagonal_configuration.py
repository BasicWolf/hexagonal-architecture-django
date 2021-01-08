from myapp.application.adapter.spi.persistence.repository.article_vote_repository import \
    ArticleVoteRepository
from myapp.application.adapter.spi.persistence.repository.vote_casting_user_repository import \
    VoteCastingUserRepository
from myapp.application.service.post_rating_service import PostRatingService


def build_production_configuration():
    _article_vote_repository = ArticleVoteRepository()
    article_vote_exists_adapter = _article_vote_repository
    save_article_vote_adapter = _article_vote_repository

    get_vote_casting_user_adapter = VoteCastingUserRepository()

    cast_article_vote_use_case = PostRatingService(
        article_vote_exists_adapter,
        get_vote_casting_user_adapter,
        save_article_vote_adapter
    )

    return {
        'cast_article_vote_use_case': cast_article_vote_use_case
    }

