from myapp.application.domain.model.vote_for_article_result import (
    VoteForArticleResult
)
from myapp.application.ports.api.vote_for_article_use_case import (
    VoteForArticleCommand,
    VoteForArticleUseCase
)
from myapp.application.ports.spi.find_article_vote_port import FindArticleVotePort
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort


class ArticleRatingService(
    VoteForArticleUseCase
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

    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        existing_article_vote = self._find_article_vote_port.find_article_vote(
            command.article_id,
            command.user_id
        )
        if existing_article_vote is not None:
            return existing_article_vote.to_already_voted_result()

        voting_user = self._find_voting_user_port.find_voting_user(
            user_id=command.user_id
        )

        vote_for_article_result, article_vote = voting_user.vote_for_article(
            command.article_id,
            command.vote
        )

        if article_vote is not None:
            self._save_article_vote_port.save_article_vote(article_vote)

        return vote_for_article_result
