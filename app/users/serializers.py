from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only
    created_by  = serializers.HiddenField(default =None)
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'role', 'password', 'created_by']  # No need for 'id' or 'is_active'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'created_by': {'write_only': True},  # Ensure created_by is write-only
        }
    def create(self, validated_data):
        # Use the manager's create_user method, which already hashes the password
        return CustomUser.objects.create_user(**validated_data)