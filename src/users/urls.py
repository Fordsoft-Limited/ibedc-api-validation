from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from core.app_url import AppUri

from .views import  (LogoutView, create_user,change_password,UserListView)

urlpatterns = [
    path(AppUri.CREATE_USER.uri, create_user, name=AppUri.CREATE_USER.uri_name),
    path(AppUri.LIST_USER.uri, UserListView.as_view(), name=AppUri.LIST_USER.uri_name),
    path(AppUri.CHANGE_PASSWORD.uri, change_password, name=AppUri.CHANGE_PASSWORD.uri_name),
    path(AppUri.LOGOUT.uri, LogoutView.as_view(), name=AppUri.LOGOUT.uri_name),
    path(AppUri.REFRESH_TOKEN.uri, TokenRefreshView.as_view(), name=AppUri.REFRESH_TOKEN.uri_name),
]