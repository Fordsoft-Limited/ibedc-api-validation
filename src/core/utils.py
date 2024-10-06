import random
import string
from rest_framework.response import Response
from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .custom_app_error import StandardApplicationException
from .constant import Notification
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def generate_batch_code():
        """
        Generate a random base62 (6 character) batch code.
        """
        chars = string.ascii_letters + string.digits  # Base62 includes a-z, A-Z, 0-9
        return ''.join(random.choices(chars, k=6))

class ApiResponse:
    def __init__(self, code=200, data=None, errorMessage=None):
        self.code = code
        self.data = data
        self.errorMessage = errorMessage
        self.status = "Success" if data is not None else "Fail"

    def get_data(self):
        """
        Return the data in the custom response format.
        """
        response = {
            "code": self.code,
            "status": self.status,
        }

        if self.data is not None:
            response["data"] = self.data

        if self.errorMessage is not None:
            response["errorMessage"] = self.errorMessage

        return response

    def to_response(self):
        """
        Return a DRF Response object.
        """
        return Response(self.get_data(), status=int(self.code))
    
    

def format_errors(errors):
    formatted_errors =""
    for field, error_list in errors.items():
        if isinstance(error_list, list) and error_list:
            formatted_errors += f"{field}: {error_list[0].__str__()}; " 
    return formatted_errors

def get_user_from_jwt_token(request):
    """
    Extract and validate the JWT token from the request header.
    Attach the user to the request object if the token is valid.
    Handle multiple exceptions like AuthenticationFailed, InvalidToken, etc.
    """
    try:
        auth = JWTAuthentication()
        user,token = auth.authenticate(request)
        if user:
            
            request.user = user
        return user 
    except InvalidToken as e:
        raise e

    except TokenError as e:
        raise e
    except AuthenticationFailed as e:
        raise e
   


    

def attach_user_to_request(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        get_user_from_jwt_token(request)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

class CustomApiRenderer(JSONRenderer):
    """
    Custom renderer to wrap responses using ApiResponse.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_status_code = renderer_context['response'].status_code
        
        # If the response already contains a custom ApiResponse, just return it
        if isinstance(data, dict) and 'code' in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Customize the response format for both success and error cases
        if response_status_code >= 400:
            # This is an error response
            api_response = ApiResponse(
                code=str(response_status_code),
                errorMessage=data.get('detail', str(data))
            )
        else:
            # This is a successful response
            api_response = ApiResponse(
                code=str(response_status_code),
                data=data
            )

        # Use ApiResponse's to_response method to convert it
        return super().render(api_response.get_data(), accepted_media_type, renderer_context)
    
