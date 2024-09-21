class ApiException(Exception):
    """Base class for custom exceptions."""
    code = "000"
    message = "An error occurred."

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"


class RecordNotFoundException(ApiException):
    def __init__(self, message="Record not found", code="404"):
        super().__init__(message, code)


class InvalidDataFormatException(ApiException):
    def __init__(self, message="Invalid data format", code="400"):
        super().__init__(message, code)


class DuplicateRecordException(ApiException):
    def __init__(self, message="Duplicate record found", code="409"):
        super().__init__(message, code)


class StandardApplicationException(ApiException):
    def __init__(self, message="Application error", code="500"):
        super().__init__(message, code)
