from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import CustomUserSerializer
from app.utils import ApiResponse, format_errors,attach_user_to_request
from app.constant import Notification
from app.custom_app_error import StandardApplicationException


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


@extend_schema(
    request=CustomUserSerializer,
    responses={201: CustomUserSerializer, 400: 'Validation Error'}
)
@api_view(['POST'])
@attach_user_to_request
@permission_classes([IsAuthenticated])
def create_user(request):
        new_account =CustomUserSerializer(data = request.data)
        if new_account.is_valid():
            new_account.save(create_by = request.user)
            return ApiResponse(data=Notification.ACCOUNT_CREATION_SUCCESS.message).to_response()
        
        raise StandardApplicationException(message=format_errors(new_account.errors), code=400)
  