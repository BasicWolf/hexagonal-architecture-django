from uuid import UUID, uuid4

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.vote_casting_user import VoteCastingUser
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    VoteCastResult, VoteAlreadyCastResult, InsufficientKarmaResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.get_vote_casting_user_port import GetVoteCastingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.post_rating_service import PostRatingService


def test_casting_valid_vote_returns_result(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            build_vote_casting_user(user_id=user_id)
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    assert isinstance(result, VoteCastResult)
    assert result.article_vote == ArticleVote(
        id=result.article_vote.id,
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )


def test_casting_same_vote_two_times_returns_vote_already_cast_result(
    user_id: UUID, article_id: UUID
):
    post_rating_service = build_post_rating_service(
        article_vote_exists_port=ArticleVoteExistsPortMock(article_exists=True)
    )
 
    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )

    assert isinstance(result, VoteAlreadyCastResult)
    assert result.vote_already_cast == VoteAlreadyCast(user_id, article_id)


def test_casting_vote_returns_insufficient_karma_handler(
    user_id: UUID,
    article_id: UUID
):
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            returned_vote_casting_user=VoteCastingUser(
                id=user_id,
                karma=2
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.UP)
    )
    assert isinstance(result, InsufficientKarmaResult)
    assert result.user_with_insufficient_karma_id == user_id


def test_cast_vote_created(
    user_id: UUID,
    article_id: UUID
):
    save_article_vote_port_mock = SaveArticleVotePortMock()
    post_rating_service = build_post_rating_service(
        get_vote_casting_user_port=GetVoteCastingUserPortMock(
            returned_vote_casting_user=build_vote_casting_user(user_id=user_id)
        ),
        save_article_vote_port=save_article_vote_port_mock
    )

    post_rating_service.cast_article_vote(
        CastArticleVoteCommand(user_id, article_id, Vote.DOWN)
    )

    saved_article_vote = save_article_vote_port_mock.saved_article_vote
    assert saved_article_vote.user_id == user_id
    assert saved_article_vote.article_id == article_id
    assert saved_article_vote.vote == Vote.DOWN


class ArticleVoteExistsPortMock(ArticleVoteExistsPort):
    def __init__(self, article_exists=False):
        self._article_exists = article_exists

    def article_vote_exists(self, user_id: UUID, article_id: UUID):
        return self._article_exists


def build_vote_casting_user(user_id: UUID = uuid4(), karma: int = 10):
    return VoteCastingUser(id=user_id, karma=karma)


class GetVoteCastingUserPortMock(GetVoteCastingUserPort):
    def __init__(
        self,
        returned_vote_casting_user: VoteCastingUser = build_vote_casting_user()
    ):
        self.returned_vote_casting_user = returned_vote_casting_user

    def get_vote_casting_user(self, user_id: UUID) -> VoteCastingUser:
        return self.returned_vote_casting_user


class SaveArticleVotePortMock(SaveArticleVotePort):
    saved_article_vote = None

    def save_article_vote(self, article_vote: ArticleVote):
        self.saved_article_vote = article_vote


def build_post_rating_service(
    article_vote_exists_port: ArticleVoteExistsPort = ArticleVoteExistsPortMock(),
    get_vote_casting_user_port: GetVoteCastingUserPort = GetVoteCastingUserPortMock(),
    save_article_vote_port: SaveArticleVotePort = SaveArticleVotePortMock()
):
    return PostRatingService(
        article_vote_exists_port=article_vote_exists_port,
        get_vote_casting_user_port=get_vote_casting_user_port,
        save_article_vote_port=save_article_vote_port
    )
