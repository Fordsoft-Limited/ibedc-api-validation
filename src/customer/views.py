# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

from core.model import DataPagination
from .serializers.upload_sl import FileUploadSerializer
from core.constant import Notification
from core.utils import ApiResponse
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from core.custom_app_error import StandardApplicationException
from core.views import BaseApiView
from .models import Customer, CustomerBatch
from .serializers.customer_sl import CustomerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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
        
@extend_schema(
    request=CustomerSerializer,
    responses={200: ApiResponse, 400: 'Validation Error'}
)        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_customer(request):
        # Create a new batch and pass it to the serializer
        batch = CustomerBatch.objects.create(
            created_by=request.user,
            validation_type='Single',
            total_record=1
        )
        customer_data = request.data
        customer_data['customer_batch'] = batch
        customer_data['created_by'] = request.user
        serializer = CustomerSerializer(data=customer_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Save will automatically handle create/update

            return ApiResponse(data="Customer processed successfully").to_response()

        return ApiResponse(errorMessage=serializer.errors, code=400).to_response()

class ListCustomerView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = DataPagination