from rest_framework import serializers

from core.custom_app_error import StandardApplicationException

from .models import CustomUser
from core.constant import Notification

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only
    created_by  = serializers.HiddenField(default =None)
    date_created = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'role', 'password', 'created_by','last_modified','date_created']  # No need for 'id' or 'is_active'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }
    def create(self, validated_data):
        # Use the manager's create_user method, which already hashes the password
        return CustomUser.objects.create_user(**validated_data)
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, min_length=5, allow_blank=False)
    new_password = serializers.CharField(max_length=50, min_length=5, allow_blank=False)
   
    def __get_login_user(self):
        return self.context['user']
    
    def validate_old_password(self, password):
        login_user = self.__get_login_user()
        if  login_user and not login_user.check_password(password):
            code, message = Notification.PASSWORD_NOT_MATCH.value
            raise StandardApplicationException(code=code, message=message)
        return password
    
    def save(self, **kwargs):
        login_user =self.__get_login_user()
        new_password = self.validated_data['new_password']
        login_user.set_password(new_password)
        login_user.save()
        return login_user
