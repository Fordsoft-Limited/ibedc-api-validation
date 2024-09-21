from enum import Enum

class AppUri(Enum):
    LOGIN = ('login/', 'login')
    LOGOUT = ('logout/', 'logout')
    CREATE_USER = ('create/', 'create_user')
    REFRESH_TOKEN = ('token/refresh/', 'refresh_token')

    def __init__(self, uri, uri_name):
        self.uri = uri
        self.uri_name = uri_name  # Using 'uri_name' for consistency with 'uri'

    @classmethod
    def get_uri(cls, uri_name):
        """Returns the URI path based on the uri_name."""
        for item in cls:
            if item.uri_name == uri_name:
                return item.uri

    @classmethod
    def get_uri_name(cls, uri):
        """Returns the URI name based on the URI path."""
        for item in cls:
            if item.uri == uri:
                return item.uri_name