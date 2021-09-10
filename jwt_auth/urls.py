from django.urls import path
from .views import RegisterView, LoginView, UserLikeView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserListView.as_view()),
    path('<int:user_pk>/like/', UserLikeView.as_view())
]
