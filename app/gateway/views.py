
from users.serializers import CustomUserSerializer
from app.utils import ApiResponse, format_errors
from app.custom_app_error import RecordNotFoundException, StandardApplicationException
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
@extend_schema(
    request=CustomUserSerializer,
    responses={201: CustomUserSerializer, 400: 'Validation Error'}
)
@api_view(['POST'])
def create_user(request):
        new_account =CustomUserSerializer(data = request.data)
        if new_account.is_valid():
            new_account.save()
            return ApiResponse(data="Signup completed").to_response()
        
        raise StandardApplicationException(message=format_errors(new_account.errors), code=400)
  