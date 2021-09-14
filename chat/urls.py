from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .chat_views import index
from .views import ProfileView, RoomView, MessageView, UserListCreateView

urlpatterns = [
    path("", index, name="home"),
    path("login/", LoginView.as_view(template_name="admin/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("api/login/", TokenObtainPairView.as_view(), name="api_login"),
    path(
        "api/user/list_create/",
        UserListCreateView.as_view(),
        name="api_user_list_create",
    ),
    path("api/token_refresh/", TokenRefreshView.as_view(), name="api_token_refresh"),
    path("api/profile/", ProfileView.as_view(), name="api_profile"),
    path("api/room/", RoomView.as_view(), name="room"),
    path("api/<str:room>/message/", MessageView.as_view(), name="message"),
]
