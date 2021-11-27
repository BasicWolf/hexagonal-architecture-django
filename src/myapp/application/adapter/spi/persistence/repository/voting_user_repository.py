from typing import Optional

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser, ArticleVote
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.ports.spi.save_voting_user_port import SaveVotingUserPort


class VotingUserRepository(
    FindVotingUserPort,
    SaveVotingUserPort
):
    def find_voting_user(self, user_id: UserId, article_id: ArticleId) -> VotingUser:
        article_vote = self._get_article_vote(user_id, article_id)
        voting_user_entity = self._get_voting_user_entity(user_id)
        return VotingUser(
            id=UserId(voting_user_entity.user_id),
            article_vote=article_vote,
            karma=Karma(voting_user_entity.karma)
        )

    def _get_article_vote(
        self,
        user_id: UserId,
        article_id: ArticleId
    ) -> Optional[ArticleVote]:
        try:
            article_vote_entity = ArticleVoteEntity.objects.get(
                user_id=user_id,
                article_id=article_id
            )
        except ArticleVoteEntity.DoesNotExist as _:
            return None

        return ArticleVote(
            ArticleId(article_vote_entity.article_id),
            Vote(article_vote_entity.vote)
        )

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e

    def save_voting_user(self, voting_user: VotingUser) -> VotingUser:
        # We are intentionally NOT creating a new VotingUser, since it's
        # a domain concept, but not necessarily a data-level concept.

        saved_article_vote: Optional[ArticleVote]
        if voting_user.voted:
            saved_article_vote = self._save_article_vote(
                voting_user.id,
                voting_user.article_vote
            )
        else:
            saved_article_vote = None

        return VotingUser(
            id=voting_user.id,
            karma=voting_user.karma,
            article_vote=saved_article_vote
        )

    def _save_article_vote(
        self,
        user_id: UserId,
        article_vote: ArticleVote
    ) -> ArticleVote:
        article_vote_entity = ArticleVoteEntity(
            article_id=article_vote.article_id,
            user_id=user_id,
            vote=article_vote.vote.value
        )
        article_vote_entity.save()
        return ArticleVote(
            ArticleId(article_vote_entity.article_id),
            Vote(article_vote_entity.vote)
        )
