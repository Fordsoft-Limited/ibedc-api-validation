from django.test import SimpleTestCase
from django.urls import reverse, resolve
from gateway.views import CustomTokenObtainPairView


class TestEntranceRouting(SimpleTestCase):
    def test_login_url(self):
        login_url = reverse('login')
        view = resolve(login_url) 
        self.assertEqual(view.func.view_class, CustomTokenObtainPairView)
