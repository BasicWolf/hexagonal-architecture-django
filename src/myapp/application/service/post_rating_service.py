from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_voting_user_port import SaveVotingUserPort


class PostRatingService(
    CastArticleVoteUseCase
):
    _find_voting_user_port: FindVotingUserPort
    _save_voting_user_port: SaveVotingUserPort

    def __init__(
        self,
        find_voting_user_port: FindVotingUserPort,
        save_voting_user_port: SaveVotingUserPort
    ):
        self._find_voting_user_port = find_voting_user_port
        self._save_voting_user_port = save_voting_user_port

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        voting_user = self._find_voting_user_port.find_voting_user(
            user_id=command.user_id,
            article_id=command.article_id
        )

        cast_vote_result = voting_user.cast_vote(command.article_id, command.vote)

        # TODO: result should be of type CastArticleVoteResult!
        if isinstance(cast_vote_result, ArticleVote):
            self._save_voting_user_port.save_voting_user(voting_user)

        return cast_vote_result
