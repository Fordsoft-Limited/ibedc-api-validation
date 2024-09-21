from rest_framework.response import Response

class ApiResponse:
    def __init__(self, code=200, data=None, errorMessage=None):
        self.code = code
        self.data = data
        self.errorMessage = errorMessage
        self.status = "Success" if data is not None else "Fail"

    def to_response(self):
        response = {
            "code": self.code,
            "status": self.status,
        }

        if self.data is not None:
            response["data"] = self.data

        if self.errorMessage is not None:
            response["errorMessage"] = self.errorMessage

        return Response(response, status=self.code)

def format_errors(errors):
    formatted_errors =""
    for field, error_list in errors.items():
        if isinstance(error_list, list) and error_list:
            formatted_errors += f"{field}: {error_list[0].__str__()}; " 
    return formatted_errors