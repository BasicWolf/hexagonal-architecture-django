from myapp.application.domain.model.vote_casting_user import InsufficientKarma, \
    CastVoteResult
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from myapp.application.ports.api.cast_article_vote.result.cast_article_vote_result import \
    CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.result.insufficient_karma_result import \
    InsufficientKarmaResult
from myapp.application.ports.api.cast_article_vote.result.vote_already_cast_result import \
    VoteAlreadyCastResult
from myapp.application.ports.api.cast_article_vote.result.vote_cast_result import \
    VoteCastResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.get_vote_casting_user_port import GetVoteCastingUserPort


class PostRatingService(
    CastArticleVoteUseCase
):
    def __init__(
        self,
        article_vote_exists_port: ArticleVoteExistsPort,
        get_vote_casting_user_port: GetVoteCastingUserPort
    ):
        self._article_vote_exists_port = article_vote_exists_port
        self._get_vote_casting_user_port = get_vote_casting_user_port

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        if self._article_vote_exists_port.article_vote_exists(
            user_id=command.user_id,
            article_id=command.article_id
        ):
            return VoteAlreadyCastResult(
                user_id=command.user_id,
                article_id=command.article_id
            )

        vote_casting_user = self._get_vote_casting_user_port.get_vote_casting_user(
            user_id=command.user_id
        )

        cast_vote_result: CastVoteResult = vote_casting_user.cast_vote(
            command.article_id,
            command.vote
        )

        if isinstance(cast_vote_result, InsufficientKarma):
            return InsufficientKarmaResult(command.user_id)

        return VoteCastResult(cast_vote_result)
