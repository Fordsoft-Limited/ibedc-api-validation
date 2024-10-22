# views.py
from rest_framework.views import APIView

from core.model import DataPagination
from .serializers.upload_sl import FileUploadSerializer
from core.utils import ApiResponse
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema
from core.custom_app_error import RecordNotFoundException, StandardApplicationException
from .models import Customer, CustomerBatch
from .serializers.customer_sl import ApproveRejectCustomerSerializer, CustomerBatchDetailSerializer, CustomerBatchSerializer, CustomerDetailsSerializer, CustomerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.utils import Notification
from customer.col import Column

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
    permission_classes =[IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            batch = serializer.save() 
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
        serializer = CustomerSerializer(data=request.data, context={"created_by": request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return ApiResponse(data="Customer processed successfully").to_response()

        return ApiResponse(errorMessage=serializer.errors, code=400).to_response()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_batch_by_user(request):
     user = request.user 
     batch_by_user = CustomerBatch.objects.filter(created_by=user.id).order_by(Column.DATE_CREATED.value)
     serializer = CustomerBatchSerializer(batch_by_user, many=True)
     return ApiResponse(data = serializer.data).to_response()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_batch_by_uid(request, uid):
     batch_by_user = CustomerBatch.objects.filter(uid=uid).order_by(Column.DATE_CREATED.value).first()
     if not batch_by_user:
          raise RecordNotFoundException(message=Notification.CUSTOMER_NOT_FOUND.message, code=Notification.CUSTOMER_NOT_FOUND.code)
     serializer = CustomerBatchDetailSerializer(batch_by_user)
     return ApiResponse(data = serializer.data).to_response()

@api_view(['GET'])
def retrieve_customer(request, uid):
     customer = Customer.objects.filter(uid=uid).order_by(Column.DATE_CREATED.value).first()
     if not customer:
          raise RecordNotFoundException(message=Notification.CUSTOMER_NOT_FOUND.message, code=Notification.CUSTOMER_NOT_FOUND.code)
     serializer = CustomerDetailsSerializer(customer)
     return ApiResponse(data = serializer.data).to_response()

@extend_schema(
    request=ApproveRejectCustomerSerializer,
    responses={200: ApiResponse, 400: 'Validation Error'}
)  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_reject_customer(request):
    serializer = ApproveRejectCustomerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        customer = serializer.customer
        serializer.update(customer, serializer.validated_data)
        return ApiResponse(data=Notification.APPROVAL_OR_REJECTION_COMPLETE.message.format(serializer.approval_status)).to_response()
    return ApiResponse(errorMessage=serializer.errors, code=400).to_response()

class ListCustomerView(ListAPIView):
    queryset = Customer.objects.all().order_by(Column.DATE_CREATED.value)
    serializer_class = CustomerSerializer
    pagination_class = DataPagination

class ListCustomerBatch(ListAPIView):
    queryset = CustomerBatch.objects.all().order_by(Column.DATE_CREATED.value)
    serializer_class = CustomerBatchSerializer
    pagination_class = DataPagination