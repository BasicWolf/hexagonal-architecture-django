from rest_framework import serializers

from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand


class CastArticleVoteCommandDeserializer(serializers.Serializer[CastArticleVoteCommand]):
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = serializers.CharField()

    # Ignored mypy error:
    # Signature of "create" incompatible with supertype "BaseSerializer"
    def create(self) -> CastArticleVoteCommand:  # type: ignore
        """
        Create and return a new `CastArticleVoteCommand` instance,
        given the validated data.
        """
        return CastArticleVoteCommand(**self.validated_data)
