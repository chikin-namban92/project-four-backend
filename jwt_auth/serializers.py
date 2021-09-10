from rest_framework import fields, serializers, status
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from floppas.serializers import LikedUserSerilizer, MessageIdSerializer, MessageSerializer, PopulatedMessageSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')
        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'does not match'})

        try:
            validation.validate_password(password=password)
        except ValidationError as err:
            raise ValidationError({'password': err.messages})

        data['password'] = make_password(password)

        return data

    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    sent_messages = MessageIdSerializer(many=True)
    liked_users = LikedUserSerilizer(many=True)
    liked_by = LikedUserSerilizer(many=True)
    class Meta:
        model = User
        fields = '__all__'
