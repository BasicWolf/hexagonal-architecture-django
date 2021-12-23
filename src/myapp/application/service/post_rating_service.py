from myapp.application.domain.model.cast_article_vote_result import (
    CastArticleVoteResult
)
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import (
    CastArticleVoteCommand,
    CastArticleVoteUseCase
)
from myapp.application.ports.spi.find_article_vote_port import FindArticleVotePort
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class PostRatingService(
    CastArticleVoteUseCase
):
    _find_article_vote_port: FindArticleVotePort
    _find_voting_user_port: FindVotingUserPort
    _save_article_vote_port: SaveArticleVotePort

    def __init__(
        self,
        find_article_vote_port: FindArticleVotePort,
        find_voting_user_port: FindVotingUserPort,
        save_article_vote_port: SaveArticleVotePort,
    ):
        self._find_article_vote_port = find_article_vote_port
        self._find_voting_user_port = find_voting_user_port
        self._save_article_vote_port = save_article_vote_port

    def cast_article_vote(self, command: CastArticleVoteCommand) -> CastArticleVoteResult:
        article_vote = self._find_article_vote_port.find_article_vote(
            command.article_id, command.user_id
        )
        if article_vote.was_already_cast:
            assert article_vote.already_cast_result is not None  # otherwise mypy warning
            return article_vote.already_cast_result

        voting_user = self._find_voting_user_port.find_voting_user(
            user_id=command.user_id,
            article_id=command.article_id
        )

        cast_vote_result = voting_user.cast_vote(command.article_id, command.vote)

        if cast_vote_result.article_vote is not None:
            self._save_article_vote_port.save_article_vote(
                cast_vote_result.article_vote
            )

        return cast_vote_result
