from myapp.application.domain.model.cast_vote_result import InsufficientKarma, \
    CastVoteResult, VoteAlreadyCast
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from myapp.application.ports.api.cast_article_vote.cast_article_vote_result import \
    CastArticleVoteResult, InsufficientKarmaResult, VoteAlreadyCastResult, VoteCastResult
from myapp.application.ports.spi.article_vote_exists_port import ArticleVoteExistsPort
from myapp.application.ports.spi.get_voting_user_port import GetVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class PostRatingService(
    CastArticleVoteUseCase
):
    _get_voting_user_port: GetVotingUserPort
    _save_article_vote_port: SaveArticleVotePort

    def __init__(
        self,
        get_voting_user_port: GetVotingUserPort,
        save_article_vote_port: SaveArticleVotePort
    ):
        self._get_voting_user_port = get_voting_user_port
        self._save_article_vote_port = save_article_vote_port

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        voting_user = self._get_voting_user_port.get_voting_user(
            user_id=command.user_id,
            article_id=command.article_id
        )

        cast_vote_result: CastVoteResult = voting_user.cast_vote(command.vote)

        if isinstance(cast_vote_result, InsufficientKarma):
            return InsufficientKarmaResult(command.user_id)
        elif isinstance(cast_vote_result, VoteAlreadyCast):
            return VoteAlreadyCastResult(
                cast_vote_user_id=command.user_id,
                cast_vote_article_id=command.article_id
            )

        self._save_article_vote_port.save_article_vote(cast_vote_result)
        return VoteCastResult(cast_vote_result)
