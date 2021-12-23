from typing import Optional
from uuid import UUID

from myapp.application.domain.model.article_vote import (
    ArticleVote,
    CastOrUncastArticleVote, UncastArticleVote
)
from myapp.application.domain.model.cast_article_vote_result import (
    InsufficientKarma,
    VoteAlreadyCast,
    VoteSuccessfullyCast
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteCommand
from myapp.application.ports.spi.find_article_vote_port import FindArticleVotePort
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.application.service.post_rating_service import PostRatingService
from tests.test_myapp.application.domain.model.builder.article_vote_creation import \
    build_article_vote
from tests.test_myapp.application.domain.model.builder.voting_user_creation import (
    build_voting_user
)
from tests.test_myapp.application.domain.model.identifier.article_id_creation import \
    create_article_id


def test_casting_valid_vote_returns_result(
    user_id: UserId,
    article_id: ArticleId
):
    post_rating_service = build_post_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            build_voting_user(user_id=user_id)
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(article_id, user_id, Vote.UP)
    )

    assert isinstance(result, VoteSuccessfullyCast)
    assert result == VoteSuccessfullyCast(
        user_id=user_id,
        article_id=article_id,
        vote=Vote.UP
    )


def test_casting_same_vote_two_times_returns_vote_already_cast_result():
    post_rating_service = build_post_rating_service(
        FindArticleVotePortStub(
            build_article_vote(
                ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
                UserId(UUID('912997c2-0000-0000-0000-000000000000'))
            )
        ),
        FindVotingUserPortStub(
            build_voting_user(UserId(UUID('912997c2-0000-0000-0000-000000000000')))
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(
            UserId(UUID('912997c2-0000-0000-0000-000000000000')),
            ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )

    assert result == VoteAlreadyCast(
        ArticleId(UUID('ef70ade4-0000-0000-0000-000000000000')),
        UserId(UUID('912997c2-0000-0000-0000-000000000000'))
    )


def test_casting_vote_returns_insufficient_karma_result(
    user_id: UserId,
    article_id: ArticleId
):
    post_rating_service = build_post_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            returned_vote_casting_user=build_voting_user(
                user_id=user_id,
                karma=Karma(2)
            )
        )
    )

    result = post_rating_service.cast_article_vote(
        CastArticleVoteCommand(article_id, user_id, Vote.UP)
    )
    assert isinstance(result, InsufficientKarma)
    assert result.user_id == user_id


def test_voting_user_saved():
    save_article_vote_port_mock = SaveArticleVotePortMock()
    post_rating_service = build_post_rating_service(
        find_voting_user_port=FindVotingUserPortStub(
            returned_vote_casting_user=build_voting_user(
                user_id=UserId(UUID('896ca302-0000-0000-0000-000000000000')),
                karma=Karma(21)
            )
        ),
        save_article_vote_port=save_article_vote_port_mock
    )

    post_rating_service.cast_article_vote(
        CastArticleVoteCommand(
            ArticleId(UUID('dd329c97-0000-0000-0000-000000000000')),
            UserId(UUID('896ca302-0000-0000-0000-000000000000')),
            Vote.DOWN
        )
    )

    saved_article_vote = save_article_vote_port_mock.saved_article_vote
    assert saved_article_vote == ArticleVote(
        ArticleId(UUID('dd329c97-0000-0000-0000-000000000000')),
        UserId(UUID('896ca302-0000-0000-0000-000000000000')),
        Vote.DOWN
    )


def test_cast_article_vote_returned_without_being_saved():
    save_article_vote_port_mock = SaveArticleVotePortMock()
    post_rating_service = build_post_rating_service(
        find_article_vote_port=FindArticleVotePortStub(
            ArticleVote(
                ArticleId(UUID('b63b6490-0000-0000-0000-000000000000')),
                UserId(UUID('4110f0fc-0000-0000-0000-000000000000')),
                Vote.UP
            )
        ),
        save_article_vote_port=save_article_vote_port_mock
    )
    post_rating_service.cast_article_vote(
        CastArticleVoteCommand(
            UserId(UUID('4110f0fc-0000-0000-0000-000000000000')),
            ArticleId(UUID('b63b6490-0000-0000-0000-000000000000')),
            Vote.UP
        )
    )
    assert save_article_vote_port_mock.saved_article_vote is None


class FindVotingUserPortStub(FindVotingUserPort):
    def __init__(
        self,
        returned_vote_casting_user: VotingUser = build_voting_user()
    ):
        self.returned_vote_casting_user = returned_vote_casting_user

    def find_voting_user(self, user_id: UserId) -> VotingUser:
        return self.returned_vote_casting_user


class SaveArticleVotePortMock(SaveArticleVotePort):
    saved_article_vote: Optional[ArticleVote] = None

    def save_article_vote(self, article_vote: ArticleVote) -> ArticleVote:
        self.saved_article_vote = article_vote
        return article_vote


class FindArticleVotePortStub(FindArticleVotePort):
    returned_article_vote: CastOrUncastArticleVote

    def __init__(
        self,
        returned_article_vote: CastOrUncastArticleVote = UncastArticleVote(
            create_article_id()
        )
    ):
        self.returned_article_vote = returned_article_vote

    def find_article_vote(
        self,
        article_id: ArticleId,
        user_id: UserId
    ) -> CastOrUncastArticleVote:
        return self.returned_article_vote


def build_post_rating_service(
    find_article_vote_port: FindArticleVotePort = FindArticleVotePortStub(),
    find_voting_user_port: FindVotingUserPort = FindVotingUserPortStub(),
    save_article_vote_port: SaveArticleVotePort = SaveArticleVotePortMock()
):
    return PostRatingService(
        find_article_vote_port,
        find_voting_user_port,
        save_article_vote_port
    )
