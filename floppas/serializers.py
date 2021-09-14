from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Chat, Message
User = get_user_model()

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'image', )

class NestedUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class LikedUserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class PopulatedMessageSerializer(MessageSerializer):
    sender = NestedUserIdSerializer()

class MessageIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text')

class ChatSerializer(serializers.ModelSerializer):
    messages_in_chat = MessageSerializer(many=True, read_only=True)
    matched_users = NestedUserSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'
