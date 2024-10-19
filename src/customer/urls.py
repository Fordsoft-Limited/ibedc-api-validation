from django.urls import path

from .views import (validate_customer , ListCustomerView,FileUploadView, list_batch_by_user,retrieve_batch_by_uid)
from core.app_url import AppUri

urlpatterns = [
    path(AppUri.CUSTOMER_BULK_VALIDATE.uri, FileUploadView.as_view(), name=AppUri.CUSTOMER_BULK_VALIDATE.uri_name),
    path(AppUri.CUSTOMER_SINGE_VALIDATE.uri, validate_customer, name=AppUri.CUSTOMER_SINGE_VALIDATE.uri_name),
    path(AppUri.CUSTOMER_LIST.uri, ListCustomerView.as_view(), name=AppUri.CUSTOMER_LIST.uri_name), 
    path(AppUri.CUSTOMER_BULK_VALIDATE_BATCH_DETAIL.uri, retrieve_batch_by_uid, name=AppUri.CUSTOMER_BULK_VALIDATE_BATCH_DETAIL.uri_name),
    path(AppUri.CUSTOMER_BULK_VALIDATE_BATCHES.uri, list_batch_by_user, name=AppUri.CUSTOMER_BULK_VALIDATE_BATCHES.uri_name),
    

]
