from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from core.model import DataPagination
from users.models import CustomUser
from .serializers import ChangePasswordSerializer, CustomUserSerializer
from core.utils import ApiResponse, format_errors,attach_user_to_request
from core.constant import Notification
from core.custom_app_error import StandardApplicationException


class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            
            # Blacklist the token
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = DataPagination

@extend_schema(
    request=CustomUserSerializer,
    responses={201: ApiResponse, 400: 'Validation Error'}
)
@api_view(['POST'])
@attach_user_to_request
@permission_classes([IsAuthenticated])
def create_user(request):
        new_account =CustomUserSerializer(data = request.data)
        if new_account.is_valid():
            new_account.save(created_by = request.user)
            return ApiResponse(data=Notification.ACCOUNT_CREATION_SUCCESS.message).to_response()
        
        raise StandardApplicationException(message=format_errors(new_account.errors), code=400)


@extend_schema(
    request=ChangePasswordSerializer,
    responses={201: ApiResponse, 400: 'Validation Error'}
)
@api_view(['POST'])
@attach_user_to_request
@permission_classes([IsAuthenticated])
def change_password(request):
        new_account =ChangePasswordSerializer(data = request.data, context={"user": request.user})
        if new_account.is_valid():
            new_account.save()
            return ApiResponse(data=Notification.PASSWORD_CHANGED.message).to_response()
        
        raise StandardApplicationException(message=format_errors(new_account.errors), code=400)
  