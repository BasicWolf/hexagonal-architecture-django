from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.cast_article_vote_result import CastArticleVoteResult
from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteUseCase
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class PostRatingService(
    CastArticleVoteUseCase
):
    _find_voting_user_port: FindVotingUserPort
    _save_article_vote_port: SaveArticleVotePort

    def __init__(
        self,
        find_voting_user_port: FindVotingUserPort,
        save_article_vote_port: SaveArticleVotePort
    ):
        self._find_voting_user_port = find_voting_user_port
        self._save_article_vote_port = save_article_vote_port

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        voting_user = self._find_voting_user_port.find_voting_user(
            user_id=command.user_id,
            article_id=command.article_id
        )

        cast_vote_result = voting_user.cast_vote(command.vote)

        if isinstance(cast_vote_result, ArticleVote):
            self._save_article_vote_port.save_article_vote(cast_vote_result)

        return cast_vote_result
