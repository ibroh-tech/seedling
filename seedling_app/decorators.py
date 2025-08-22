from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def handle_exceptions(func):
    """
    A decorator to handle exceptions in API views and return appropriate responses.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e), "details": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper
