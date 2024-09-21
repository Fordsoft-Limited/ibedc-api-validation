from django.urls import path

from .views import CustomTokenObtainPairView, create_user
from app.app_url import AppUri

urlpatterns = [
    path(AppUri.LOGIN.uri, CustomTokenObtainPairView.as_view(), name=AppUri.LOGIN.uri_name),
    path(AppUri.CREATE_USER.uri, create_user, name=AppUri.CREATE_USER.uri_name)
]