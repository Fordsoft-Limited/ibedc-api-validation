# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
# from django.core.files.base import ContentFile
from .serializers import FileUploadSerializer
from app.constant import Notification
from app.utils import ApiResponse
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from app.custom_app_error import StandardApplicationException

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'format': 'binary'},
                'constraints': {'type': 'string'},
            },
            'required': ['file']
        }
    },
    responses={201: 'Success', 400: 'Bad Request'}
)
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file']
            external_file_path = os.path.join(settings.EXTERNAL_STORAGE_ROOT, file.name)
            with open(external_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return ApiResponse(data=Notification.FILE_UPLOADED.message).to_response()
        else:
            raise StandardApplicationException(message=serializer.errors, code=400)
