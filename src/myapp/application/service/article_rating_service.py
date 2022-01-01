from myapp.application.domain.event.user_voted_event import UserVotedEvent
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote_for_article_result import (
    VoteForArticleResult
)
from myapp.application.ports.api.vote_for_article_use_case import (
    VoteForArticleCommand,
    VoteForArticleUseCase
)
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_article_vote_port import SaveArticleVotePort
from myapp.eventlib.event_dispatcher import EventDispatcher


class ArticleRatingService(
    VoteForArticleUseCase
):
    _find_voting_user_port: FindVotingUserPort
    _save_article_vote_port: SaveArticleVotePort
    _domain_event_dispatcher: EventDispatcher

    def __init__(
        self,
        find_voting_user_port: FindVotingUserPort,
        save_article_vote_port: SaveArticleVotePort,
        domain_event_dispatcher: EventDispatcher
    ):
        self._find_voting_user_port = find_voting_user_port
        self._save_article_vote_port = save_article_vote_port
        self._domain_event_dispatcher = domain_event_dispatcher
        self._domain_event_dispatcher.register_handler(
            UserVotedEvent,
            self._on_user_voted
        )

    def vote_for_article(self, command: VoteForArticleCommand) -> VoteForArticleResult:
        voting_user = self._find_voting_user_port.find_voting_user(
            command.article_id,
            command.user_id
        )

        vote_for_article_result, events = voting_user.vote_for_article(
            command.article_id,
            command.vote
        )

        for event in events:
            self._domain_event_dispatcher.dispatch(event)

        return vote_for_article_result

    def _on_user_voted(self, event: UserVotedEvent):
        self._save_article_vote_port.save_article_vote(
            ArticleVote(
                event.article_id,
                event.user_id,
                event.vote
            )
        )
