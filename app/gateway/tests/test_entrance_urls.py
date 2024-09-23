from django.test import SimpleTestCase
from django.urls import reverse, resolve
from gateway.views import CustomTokenObtainPairView
from app.app_url import AppUri 


class TestEntranceRouting(SimpleTestCase):
    def test_login_url(self):
        login_url = reverse(AppUri.LOGIN.uri_name)
        view = resolve(login_url) 
        self.assertEqual(view.func.view_class, CustomTokenObtainPairView)
