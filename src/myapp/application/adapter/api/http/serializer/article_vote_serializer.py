from rest_enumfield import EnumField
from rest_framework import serializers

from myapp.application.domain.model.cast_article_vote_result import VoteCast
from myapp.application.domain.model.vote import Vote


class VoteCastSerializer(serializers.Serializer[VoteCast]):
    user_id = serializers.UUIDField()
    article_id = serializers.UUIDField()
    vote = EnumField(Vote)
