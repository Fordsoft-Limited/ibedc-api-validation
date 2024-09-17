from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get the default token from the parent class
        token = super().get_token(user)

        # Add custom claims (extra information) to the token
        token['name'] = user.name
        token['role'] = user.role
        token['is_active'] = user.is_active

        return token

    def validate(self, attrs):
        # Get the original response data (access and refresh tokens)
        data = super().validate(attrs)

        # Add additional user details to the response (besides the token itself)
        data['name'] = self.user.name
        data['role'] = self.user.role
        data['is_active'] = self.user.is_active

        return data
