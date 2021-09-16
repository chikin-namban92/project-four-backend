from django.urls import path
from .views import ChatListView, MessageListView, MessagePostView

urlpatterns = [
    path('chat/', ChatListView.as_view()),
    # path('chat/<int:chat_pk>/message/', ChatDetailView.as_view()),
    path('chat/message', MessageListView.as_view()),
    path('chat/<int:chat_pk>/message/', MessagePostView.as_view())
]
