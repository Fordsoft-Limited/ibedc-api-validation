# views.py
from rest_framework.views import APIView

from core.model import DataPagination
from .serializers.upload_sl import FileUploadSerializer
from core.utils import ApiResponse
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema
from core.custom_app_error import StandardApplicationException
from .models import Customer, CustomerBatch
from .serializers.customer_sl import CustomerBatchDetailSerializer, CustomerBatchSerializer, CustomerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.utils import Notification

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
        serializer = FileUploadSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            batch = serializer.save() 
            return ApiResponse(data=Notification.FILE_UPLOADED).to_response()
        else:
            raise StandardApplicationException(message=serializer.errors, code=400)
        
@extend_schema(
    request=CustomerSerializer,
    responses={200: ApiResponse, 400: 'Validation Error'}
)        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_customer(request):
        serializer = CustomerSerializer(data=request.data, context={"created_by": request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return ApiResponse(data="Customer processed successfully").to_response()

        return ApiResponse(errorMessage=serializer.errors, code=400).to_response()

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_batch_by_user(request):
     user = request.user 
     batch_by_user = CustomerBatch.objects.filter(created_by=user.id)
     serializer = CustomerBatchSerializer(batch_by_user, many=True)
     return ApiResponse(data = serializer.data).to_response()

@api_view(['GET'])
def retrieve_batch_by_uid(request, uid):
     batch_by_user = CustomerBatch.objects.filter(uid=uid).first()
     serializer = CustomerBatchDetailSerializer(batch_by_user)
     return ApiResponse(data = serializer.data).to_response()

class ListCustomerView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = DataPagination