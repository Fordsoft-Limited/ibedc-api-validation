from django.urls import path

from .views import validate_customer , ListCustomerView,FileUploadView
from core.app_url import AppUri

urlpatterns = [
    path(AppUri.CUSTOMER_BULK_VALIDATE.uri, FileUploadView.as_view(), name=AppUri.CUSTOMER_BULK_VALIDATE.uri_name),
    path(AppUri.CUSTOMER_SINGE_VALIDATE.uri, validate_customer, name=AppUri.CUSTOMER_SINGE_VALIDATE.uri_name),
    path(AppUri.CUSTOMER_LIST.uri, ListCustomerView.as_view(), name=AppUri.CUSTOMER_LIST.uri_name)
]
