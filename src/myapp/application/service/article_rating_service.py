from django.db import transaction

from myapp.application.domain.model.vote_for_article_result import (
    SuccessfullyVotedResult, VoteForArticleResult
)
from myapp.application.ports.api.command.vote_for_article_command import (
    VoteForArticleCommand
)
from myapp.application.ports.api.vote_for_article_use_case import (
    VoteForArticleUseCase
)
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_voting_user_port import SaveVotingUserPort


class ArticleRatingService(
    VoteForArticleUseCase
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

    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        with transaction.atomic():
            return self._vote_for_article(command)

    def _vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        voting_user = self._find_voting_user_port.find_voting_user(
            command.article_id,
            command.user_id
        )

        voting_result = voting_user.vote_for_article(
            command.article_id,
            command.vote
        )

        match voting_result:
            case SuccessfullyVotedResult():
                self._save_voting_user_port.save_voting_user(voting_user)

        return voting_result
