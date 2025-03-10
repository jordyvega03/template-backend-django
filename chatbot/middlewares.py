from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """ Manejador global de excepciones para respuestas JSON personalizadas """

    response = exception_handler(exc, context)

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({
            "status": 401,
            "message": "No tienes autorización para acceder a este recurso. Por favor, proporciona un token válido.",
            "errors": []
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response
