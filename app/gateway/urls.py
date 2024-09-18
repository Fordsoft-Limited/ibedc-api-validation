from django.urls import path

from .views import CustomTokenObtainPairView
from app.app_url import AppUri

urlpatterns = [
    path(AppUri.LOGIN.uri, CustomTokenObtainPairView.as_view(), name=AppUri.LOGIN.uri_name)
]