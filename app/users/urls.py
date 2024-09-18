from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from app.app_url import AppUri

from .views import  LogoutView

urlpatterns = [
    path(AppUri.LOGOUT.uri, LogoutView.as_view(), name=AppUri.LOGOUT.uri_name),
    path(AppUri.REFRESH_TOKEN.uri, TokenRefreshView.as_view(), name=AppUri.REFRESH_TOKEN.uri_name),
]