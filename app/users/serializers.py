from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'role', 'password']  # No need for 'id' or 'is_active'

    def create(self, validated_data):
        # Use the manager's create_user method, which already hashes the password
        return CustomUser.objects.create_user(**validated_data)