from rest_framework import serializers
from .models import FriendRequest
from account.models import User


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True)
    receiver = serializers.CharField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'is_accepted']
        read_only_fields = ['sender', 'receiver', 'is_accepted']

    def create(self, validated_data):
        return super().create(validated_data)


class FriendRequestActionSerializer(serializers.Serializer):
    ACTION_CHOICES = (
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )
    action = serializers.ChoiceField(choices=ACTION_CHOICES)

class ListFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']