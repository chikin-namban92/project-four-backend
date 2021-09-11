from django.urls import path
from .views import ChatListView

urlpatterns = [
    path('chat/', ChatListView.as_view())
]
