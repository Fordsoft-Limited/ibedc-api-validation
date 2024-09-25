from enum import Enum
class Notification(Enum):
    AUTHENTICATION_FAIL = (401, 'Authentication failed: Invalid credentials provided.')
    AUTHORIZATION_FAIL = (403, 'Authorization failed: Access is denied due to insufficient permissions.')
    LOGIN_FAIL = (404, 'Login failed: Either username or password is incorrect.')
    ACCOUNT_CREATION_SUCCESS = (201, 'Success! Your account has been successfully created.')
    PASSWORD_NOT_MATCH = (400, 'Old password not match existing password')
    PASSWORD_CHANGED = (200, 'Password changed successfully')
    FILE_UPLOADED = (200, 'File uploaded successfully')
   

    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def get_message(self):
        return f"Error {self.code}: {self.message}"