from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# class CommentListView(APIView):
#     permission_classes = (IsAuthenticated, ):

#     def post(self, request, chat_pk)
