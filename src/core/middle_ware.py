from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser  # Import AnonymousUser
from .utils import get_user_from_jwt_token

class AttachUserMiddleware(MiddlewareMixin):
    """
    Middleware to attach user to request object using JWT token in the Authorization header.
    If no valid token is provided, the user will be set to AnonymousUser.
    """

    def process_request(self, request):
        # Extract the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            try:
                # Extract user from JWT token
                user = get_user_from_jwt_token(request)
                
                # Attach the authenticated user to the request object
                request.user = user

            except AuthenticationFailed:
                # If the token is invalid, set the user to AnonymousUser
                request.user = AnonymousUser()

        else:
            # If no auth header, set user to AnonymousUser
            request.user = AnonymousUser()
