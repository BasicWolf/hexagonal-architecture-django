from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_vote_result import CastVoteResult
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
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

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastVoteResult:
        voting_user = self._get_voting_user_port.get_voting_user(
            user_id=command.user_id,
            article_id=command.article_id
        )

        cast_vote_result: CastVoteResult = voting_user.cast_vote(command.vote)

        if isinstance(cast_vote_result, ArticleVote):
            self._save_article_vote_port.save_article_vote(cast_vote_result)

        return cast_vote_result
