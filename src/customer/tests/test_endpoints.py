from django.test import SimpleTestCase
from django.urls import reverse, resolve
from customer.views import  (FileUploadView)
from core.app_url import AppUri

class TestCustomerEndpoint(SimpleTestCase):
    def test_upload(self):
        url = reverse(AppUri.FILE_UPLOAD.uri_name)
        view = resolve(url)
        self.assertEqual(view.func.view_class, FileUploadView)

