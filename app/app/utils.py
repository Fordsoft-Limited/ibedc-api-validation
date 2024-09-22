from rest_framework.response import Response
from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .custom_app_error import StandardApplicationException
from .constant import Notification

class ApiResponse:
    def __init__(self, code=200, data=None, errorMessage=None):
        self.code = code
        self.data = data
        self.errorMessage = errorMessage
        self.status = "Success" if data is not None else "Fail"

    def to_response(self):
        response = {
            "code": self.code,
            "status": self.status,
        }

        if self.data is not None:
            response["data"] = self.data

        if self.errorMessage is not None:
            response["errorMessage"] = self.errorMessage

        return Response(response, status=self.code)

def format_errors(errors):
    formatted_errors =""
    for field, error_list in errors.items():
        if isinstance(error_list, list) and error_list:
            formatted_errors += f"{field}: {error_list[0].__str__()}; " 
    return formatted_errors



def attach_user_to_request(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract and validate the JWT token from the request header
        try:
            auth = JWTAuthentication()
            # This will return a tuple (user, validated_token)
            user, token = auth.authenticate(request)
            if user:
                # Attach the user to the request
                request.user = user
        except AuthenticationFailed:
            code, message = Notification.AUTHENTICATION_FAIL.value
            raise StandardApplicationException(message=message, status=code)

        return view_func(request, *args, **kwargs)

    return _wrapped_view