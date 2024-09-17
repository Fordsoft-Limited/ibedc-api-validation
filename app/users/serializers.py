from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from app.users.models import CustomUser

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
    
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'role', 'password']  # No need for 'id' or 'is_active'

    def create(self, validated_data):
        # Use the manager's create_user method, which already hashes the password
        return CustomUser.objects.create_user(**validated_data)