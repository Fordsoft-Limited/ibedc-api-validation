from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

        # Add additional user details to the response (besides the token itself)
        data['name'] = self.user.name
        data['role'] = self.user.role
        data['slug'] = self.user.slug
        data['username'] = self.user.username
        data['is_active'] = self.user.is_active

        return data
    