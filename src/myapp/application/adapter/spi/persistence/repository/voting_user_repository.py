from typing import Optional

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import \
    ArticleVoteEntity
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import \
    VotingUserEntity
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import \
    VotingUserNotFound
from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort


class VotingUserRepository(
    FindVotingUserPort
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
        except ArticleVoteEntity.DoesNotExist:
            return None

        return ArticleVote(
            ArticleId(article_vote_entity.article_id),
            UserId(article_vote_entity.user_id),
            Vote(article_vote_entity.vote)
        )

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e
