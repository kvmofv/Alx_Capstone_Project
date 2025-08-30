from django.urls import path
from .views import (LoginAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView,)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:id>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:id>/update/", UserUpdateAPIView.as_view(), name="user-update"),
]
