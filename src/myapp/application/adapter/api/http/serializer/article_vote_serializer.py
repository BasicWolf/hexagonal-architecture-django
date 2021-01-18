from rest_framework import serializers

from myapp.application.domain.model.article_vote import ArticleVote


class ArticleVoteSerializer(serializers.Serializer[ArticleVote]):
    id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = serializers.CharField()
