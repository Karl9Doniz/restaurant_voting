from rest_framework import serializers
from core.models import Restaurant, Menu, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ["employee"]


class VotingResultSerializer(serializers.Serializer):
    menu = serializers.StringRelatedField()
    vote_count = serializers.IntegerField()
    votes = VoteSerializer(many=True)
