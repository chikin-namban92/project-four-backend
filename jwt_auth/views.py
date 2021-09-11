from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from floppas.models import Chat

from .serializers import UserProfileSerializer, UserRegisterSerializer
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserRegisterSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message': 'Registration Successful'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(username=username)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Unauthorized')

        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Unauthorized')

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            { 'sub': user_to_login.id, 'exp': int(expiry_time.strftime('%s')) },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({
            'token': token,
            'message': f'Welcome back {username}'
        }, status=status.HTTP_200_OK)

# class ProfileView(APIView):

#     permission_classes = (IsAuthenticated, )

#     def get(self, request):
#         serialized_user = UserProfileSerializer(request.user)
#         return Response(serialized_user.data, status=status.HTTP_200_OK)

class UserListView(APIView):
    def get(self, _request):
        users = User.objects.all()
        serialized = UserProfileSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class UserLikeView(APIView):
    ''' Adds user to liked_users and vice versa and removes if already liked '''
    permission_classes = (IsAuthenticated, )

    def post(self, request, user_pk):
        try:
            user_to_like = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFound()

        if request.user in user_to_like.liked_by.all():
            user_to_like.liked_by.remove(request.user.id)
        else:
            user_to_like.liked_by.add(request.user.id)

        if (
            request.user in user_to_like.liked_by.all()
            ) and (
                request.user in user_to_like.liked_users.all()
                ):
            chat_to_create = Chat.objects.create()
            chat_to_create.matched_users.add(request.user.id, user_to_like)

        return Response(status=status.HTTP_202_ACCEPTED)
