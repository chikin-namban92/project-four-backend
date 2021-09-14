from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from jwt_auth.models import User

from floppas.serializers import ChatSerializer, MessageSerializer, NestedUserSerializer, PopulatedMessageSerializer
from floppas.models import Chat

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

class MessageListView(APIView):
    ''' List / Create View for Messages '''

    permission_classes = (IsAuthenticated, )

    def post(self, request, chat_pk):
        request.data['parent_chat'] = chat_pk
        request.data['sender'] = request.user.id
        created_message = MessageSerializer(data=request.data)
        if created_message.is_valid():
            created_message.save()
            return Response(created_message.data, status=status.HTTP_201_CREATED)
        return Response(
            created_message.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
