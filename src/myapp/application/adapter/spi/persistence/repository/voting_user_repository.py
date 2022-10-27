from typing import cast, List, Optional

from myapp.application.adapter.spi.persistence.entity.article_vote_entity import (
    ArticleVoteEntity
)
from myapp.application.adapter.spi.persistence.entity.voting_user_entity import (
    VotingUserEntity
)
from myapp.application.adapter.spi.persistence.exceptions.voting_user_not_found import (
    VotingUserNotFound
)
from myapp.application.domain.model.identifier.article_id import ArticleId
from myapp.application.domain.model.identifier.user_id import UserId
from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.vote import Vote
from myapp.application.domain.model.voting_user import ArticleVote, VotingUser
from myapp.application.port.spi.find_voting_user_port import FindVotingUserPort
from myapp.application.port.spi.save_voting_user_port import SaveVotingUserPort


class VotingUserRepository(
    FindVotingUserPort,
    SaveVotingUserPort
):
    def find_voting_user(self, article_id: ArticleId, user_id: UserId) -> VotingUser:
        voting_user_entity = self._get_voting_user_entity(user_id)
        article_vote: Optional[ArticleVote] = self._get_article_vote(article_id, user_id)

        return VotingUser(
            user_id,
            Karma(voting_user_entity.karma),
            [article_vote] if article_vote is not None else []
        )

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            # Annotations can be used to add `voted` field to the returned result,
            # but we want to keep things simple and clear.
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e

    def _get_article_vote(
        self,
        article_id: ArticleId,
        user_id: UserId
    ) -> ArticleVote | None:
        article_vote_entity = ArticleVoteEntity.objects.filter(
            article_id=article_id,
            user_id=user_id
        ).first()

        return self._article_entity_to_domain_model(article_vote_entity) if (
            article_vote_entity is not None
        ) else (
            None
        )

    def old_save_voting_user(self, voting_user: VotingUser) -> VotingUser:
        VotingUserEntity(
            user_id=voting_user.id,
            karma=voting_user.karma
        ).save()

        for article_vote in voting_user.votes_for_articles:
            self._article_vote_to_entity(article_vote).save()

        return voting_user

    def save_voting_user(self, voting_user: VotingUser) -> VotingUser:
        voting_user_entity = self._voting_user_to_entity(voting_user)
        voting_user_entity.save()
        saved_votes_for_articles = self._save_votes_for_articles(
            voting_user.votes_for_articles
        )

        return self._voting_user_entity_to_domain_model(
            voting_user_entity,
            saved_votes_for_articles
        )

    def _save_votes_for_articles(
        self,
        votes_for_articles: List[ArticleVote]
     ) -> List[ArticleVote]:
        saved_votes: List[ArticleVote] = []

        for article_vote in votes_for_articles:
            article_vote_entity = self._article_vote_to_entity(article_vote)
            article_vote_entity.save()
            saved_vote = self._article_entity_to_domain_model(article_vote_entity)
            saved_votes.append(saved_vote)

        return saved_votes

    def _voting_user_to_entity(self, voting_user: VotingUser) -> VotingUserEntity:
        return VotingUserEntity(
            user_id=voting_user.id,
            karma=voting_user.karma
        )

    def _voting_user_entity_to_domain_model(
        self,
        voting_user_entity: VotingUserEntity,
        votes_for_articles: List[ArticleVote]
    ) -> VotingUser:
        return VotingUser(
            UserId(voting_user_entity.user_id),
            karma=Karma(voting_user_entity.karma),
            votes_for_articles=votes_for_articles
        )

    def _article_vote_to_entity(self, article_vote: ArticleVote) -> ArticleVoteEntity:
        return ArticleVoteEntity(
            article_id=article_vote.article_id,
            user_id=article_vote.user_id,
            vote=cast(str, article_vote.vote)
        )

    def _article_entity_to_domain_model(self, entity: ArticleVoteEntity) -> ArticleVote:
        return ArticleVote(
            ArticleId(entity.article_id),
            UserId(entity.user_id),
            Vote(entity.vote)
        )
