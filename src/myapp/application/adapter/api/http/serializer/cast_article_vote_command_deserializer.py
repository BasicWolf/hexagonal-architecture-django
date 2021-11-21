from rest_enumfield import EnumField
from rest_framework import serializers

from myapp.application.domain.model.vote import Vote
from myapp.application.ports.api.cast_article_vote.cast_aticle_vote_use_case import \
    CastArticleVoteCommand


class CastArticleVoteCommandDeserializer(serializers.Serializer[CastArticleVoteCommand]):
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = EnumField(Vote)

    # Ignored mypy error:
    # Signature of "create" incompatible with supertype "BaseSerializer"
    def create(self) -> CastArticleVoteCommand:  # type: ignore
        """
        Create and return a new `CastArticleVoteCommand` instance,
        given the validated data.
        """
        return CastArticleVoteCommand(**self.validated_data)
