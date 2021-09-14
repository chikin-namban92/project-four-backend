from django.urls import path
from .views import ChatListView, MessageListView

urlpatterns = [
    path('chat/', ChatListView.as_view()),
    path('chat/<int:chat_pk>/message/', MessageListView.as_view())
]
