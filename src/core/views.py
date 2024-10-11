from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class BaseApiView(APIView):
    """
    Base API view that enforces IsAuthenticated permission.
    All other views can inherit from this view.
    """
    permission_classes = [IsAuthenticated]
