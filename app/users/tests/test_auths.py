from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.users.views import  LogoutView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from app.app_url import AppUri

class TestAuths(SimpleTestCase):
    def test_logout(self):
        logout_url = reverse(AppUri.LOGOUT.name)
        logout_view = resolve(logout_url)
        self.assertEqual(logout_view.func.view_class, LogoutView)
    def test_refresh_token(self):
        token_refresh_url = reverse(AppUri.REFRESH_TOKEN.name)
        view = resolve(token_refresh_url)
        self.assertEqual(view.func.view_class, TokenRefreshView)
