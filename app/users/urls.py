from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import CustomTokenObtainPairView, LogoutView

urlpatterns = [
    # JWT Token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]