from rest_framework import serializers

from myapp.application.ports.api.cast_article_vote.cast_article_vote_command import \
    CastArticleVoteCommand


class CastArticleVoteCommandDeserializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = serializers.CharField()

    def create(self) -> CastArticleVoteCommand:
        """
        Create and return a new `CastArticleVoteCommand` instance,
        given the validated data.
        """
        return CastArticleVoteCommand(**self.validated_data)
