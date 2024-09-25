from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.utils import ApiResponse
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get the default token from the parent class
        token = super().get_token(user)

        # Add custom claims (extra information) to the token
        token['name'] = user.name
        token['role'] = user.role
        token['slug'] = user.slug
        token['username'] = user.username
        token['is_active'] = user.is_active

        return token

    def validate(self, attrs):
        # Get the original response data (access and refresh tokens)
        data = super().validate(attrs)
        user_data = {
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'name': self.user.name,
            'role': self.user.role,
            'slug': self.user.slug,
            'username': self.user.username,
            'is_active': self.user.is_active
        }
     
        return  user_data
    