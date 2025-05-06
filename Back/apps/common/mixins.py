from rest_framework.response import Response
from rest_framework import status

class CustomResponseMixin:
    """
    Mixin to standardize API responses.
    """
    def success_response(self, data, message="Success", status_code=status.HTTP_200_OK):
        return Response({"message": message, "data": data}, status=status_code)
    
    def error_response(self, errors, message="Error", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message, "errors": errors}, status=status_code)
