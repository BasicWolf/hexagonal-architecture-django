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
from myapp.application.domain.model.voting_user import VotingUser
from myapp.application.ports.spi.find_voting_user_port import FindVotingUserPort


class VotingUserRepository(FindVotingUserPort):
    def find_voting_user(self, user_id: UserId, article_id: ArticleId) -> VotingUser:
        vote = self._get_vote(user_id, article_id)
        voting_user_entity = self._get_voting_user_entity(user_id)
        return VotingUser(
            id=UserId(voting_user_entity.user_id),
            voting_for_article_id=ArticleId(article_id),
            vote=vote,
            karma=Karma(voting_user_entity.karma)
        )

    def _get_vote(self, user_id: UserId, article_id: ArticleId) -> Vote:
        try:
            article_vote_entity_vote = ArticleVoteEntity.objects.filter(
                user_id=user_id,
                article_id=article_id
            ).values(
                'vote'
            ).get()['vote']
            return ArticleVoteEntity.vote_to_domain_model(article_vote_entity_vote)
        except ArticleVoteEntity.DoesNotExist as _:
            return Vote.NOT_VOTED

    def _get_voting_user_entity(self, user_id: UserId) -> VotingUserEntity:
        try:
            return VotingUserEntity.objects.get(user_id=user_id)
        except VotingUserEntity.DoesNotExist as e:
            raise VotingUserNotFound(user_id) from e
