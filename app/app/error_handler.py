from rest_framework.views import exception_handler
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.urls import Resolver404
from .custom_app_error import ApiException
from .utils import ApiResponse
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .constant import Notification

def custom_exception_handler(exc, context):
    # Handle custom exceptions
    if isinstance(exc, ApiException):
        # Use the actual message and status code from the custom exception
        response = ApiResponse(code=exc.code, errorMessage=str(exc.message))
        return response.to_response()

    # Handle Django's Http404 Exception
    if isinstance(exc, Http404):
        # Real message from the exception or provide a default message if necessary
        response = ApiResponse(code="404", errorMessage=str(exc) or "Record not found")
        return response.to_response()
     # Handle Django's Http404 Exception
    if isinstance(exc, AuthenticationFailed):
        # Real message from the exception or provide a default message if necessary
        code, message = Notification.AUTHORIZATION_FAIL.value
        response = ApiResponse(code=code, errorMessage=str(exc) or message)
        return response.to_response()
    if isinstance(exc, NotAuthenticated):
        # Real message from the exception or provide a default message if necessary
        code, message = Notification.AUTHORIZATION_FAIL.value
        response = ApiResponse(code=code, errorMessage=str(exc) or message)
        return response.to_response()
    # Handle Resolver404 (endpoint not found)
    if isinstance(exc, Resolver404):
        # Extract message from the exception
        response = ApiResponse(code="404", errorMessage=str(exc) or "Endpoint not found")
        return response.to_response()

    # Handle Django's PermissionDenied Exception
    if isinstance(exc, PermissionDenied):
        # Extract the actual message
        response = ApiResponse(code="403", errorMessage=str(exc) or "Permission denied")
        return response.to_response()

    # Handle Django's and DRF's ValidationError
    if isinstance(exc, (DjangoValidationError, DRFValidationError)):
        # Extract the validation error messages
        error_message = getattr(exc, 'detail', str(exc))
        response = ApiResponse(code="400", errorMessage=error_message)
        return response.to_response()

    # Handle Python's ValueError
    if isinstance(exc, ValueError):
        # Use the actual message from the exception
        response = ApiResponse(code="400", errorMessage=str(exc) or "Invalid data")
        return response.to_response()

    # Handle other unhandled exceptions using DRF's exception handler
    response = exception_handler(exc, context)

    # If DRF didn't handle the exception, return a generic 500 error
    if response is None:
        # Provide default error message only for internal server errors
        response = ApiResponse(code="500", errorMessage="An internal server error occurred.")
        return response.to_response()

    # For other errors, use the DRF-generated response
    return response
