import uuid
from django.db import models
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class DataPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'  
    max_page_size = 200  