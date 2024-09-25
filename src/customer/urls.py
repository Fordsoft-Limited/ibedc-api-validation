from django.urls import path

from .views import FileUploadView
from core.app_url import AppUri

urlpatterns = [
    path(AppUri.FILE_UPLOAD.uri, FileUploadView.as_view(), name=AppUri.FILE_UPLOAD.uri_name)
]