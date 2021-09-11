from rest_framework import status
from rest_framework.response import Response
from floppas.models import Chat
from rest_framework.exceptions import NotFound
from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from jwt_auth.models import User

from floppas.serializers import ChatSerializer

class ChatListView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        chats = Chat.objects.all()
        serialized = ChatSerializer(chats, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

# class ChatDetailView(RetrieveAPIView):
#     ''' Detail View for /characters/id SHOW UPDATE DELETE'''
#     permission_classes = (IsAuthenticated, )

#     def get(self, request, chat_pk):
#         request.data['chat'] = chat_pk
#         serialized_chat = ChatSerializer(request.chat)
#         return Response(serialized_chat)

        

class UserMatchView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, user_pk):
        liked_user = User.objects.get(pk=user_pk)
        self.matched_users.add(request.user.id, liked_user)

class UserUnmatchView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, user_pk):
        liked_user = User.objects.get(pk=user_pk)
        self.matched_users.remove(request.user.id, liked_user)
