from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser  # Import AnonymousUser
from .utils import get_user_from_jwt_token

class AttachUserMiddleware(MiddlewareMixin):
    """
    Middleware to attach user to request object using JWT token in the Authorization header.
    If no valid token is provided and the user is not authenticated via session, the user will be set to AnonymousUser.
    """

    def process_request(self, request):
        # Check if the user is already authenticated (e.g., session-based login)
        if request.user.is_authenticated:
            return  # Skip JWT processing if the user is already authenticated

        # Extract the Authorization header for JWT-based authentication
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            try:
                # Extract user from JWT token
                user = get_user_from_jwt_token(request)

                # Attach the authenticated user from JWT to the request object
                request.user = user

            except AuthenticationFailed:
                # If the token is invalid, set the user to AnonymousUser
                request.user = AnonymousUser()

        else:
            # If no auth header and user is not authenticated, set user to AnonymousUser
            request.user = AnonymousUser()
