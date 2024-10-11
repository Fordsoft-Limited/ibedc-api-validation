from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import  (logout, create_user, change_password)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from core.app_url import AppUri

class TestEndpoint(SimpleTestCase):
    def test_logout(self):
        logout_url = reverse(AppUri.LOGOUT.uri_name)
        logout_view = resolve(logout_url)
        self.assertEqual(logout_view.func, logout)
    def test_refresh_token(self):
        token_refresh_url = reverse(AppUri.REFRESH_TOKEN.uri_name)
        view = resolve(token_refresh_url)
        self.assertEqual(view.func.view_class, TokenRefreshView)
    def test_create_user(self):
        create_user_uri = reverse(AppUri.CREATE_USER.uri_name)
        view = resolve(create_user_uri)
        self.assertEqual(view.func, create_user)
    def test_change_password(self):
        uri = reverse(AppUri.CHANGE_PASSWORD.uri_name)
        view = resolve(uri)
        self.assertEqual(view.func, change_password)