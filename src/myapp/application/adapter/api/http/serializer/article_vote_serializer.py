from rest_enumfield import EnumField
from rest_framework import serializers

from myapp.application.domain.model.article_vote import ArticleVote
from myapp.application.domain.model.vote import Vote


class ArticleVoteSerializer(serializers.Serializer[ArticleVote]):
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = EnumField(Vote)
