from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserSerializer, ConversationSerializer, MessageSerializer, ChatLogSerializer, TokenSerializer, \
    UploadFileSerializer, ChatbotConfigSerializer, ApiResponse
from .models import User, Conversation, Message, ChatbotConfig, ChatLog, Token, UploadFile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from .models import User


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Tienes acceso con JWT"}, status=200)

class BaseViewSet(viewsets.ModelViewSet):
    """ Clase base para heredar métodos de manejo de respuestas y errores """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """ Obtiene la lista de elementos """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message=f"Lista de {self.queryset.model.__name__.lower()} obtenida")

    def retrieve(self, request, *args, **kwargs):
        """ Obtiene un elemento por ID """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return ApiResponse.success(data=serializer.data, message=f"{self.queryset.model.__name__} encontrado")
        except Http404:
            return ApiResponse.error(message=f"{self.queryset.model.__name__} no encontrado", status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """ Crea un nuevo elemento """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message=f"{self.queryset.model.__name__} creado correctamente",
                                       status=status.HTTP_201_CREATED)
        return ApiResponse.error(errors=serializer.errors, message=f"Error al crear {self.queryset.model.__name__.lower()}",
                                 status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ Actualiza un elemento existente """
        try:
            instance = self.get_object()
        except Http404:
            return ApiResponse.error(message=f"{self.queryset.model.__name__} no encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message=f"{self.queryset.model.__name__} actualizado correctamente")
        return ApiResponse.error(errors=serializer.errors, message=f"Error al actualizar {self.queryset.model.__name__.lower()}",
                                 status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Elimina un elemento """
        try:
            instance = self.get_object()
        except Http404:
            return ApiResponse.error(message=f"{self.queryset.model.__name__} no encontrado", status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return ApiResponse.success(message=f"{self.queryset.model.__name__} eliminado correctamente", status=status.HTTP_204_NO_CONTENT)

    def permission_denied(self, request, message=None, code=None):
        """ Maneja el caso en que el usuario no tiene permisos """
        if isinstance(message, NotAuthenticated):
            return ApiResponse.error(
                message="No tienes autorización para acceder a este recurso",
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().permission_denied(request, message, code)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Define los permisos de cada acción:
        - `register` y `login` no requieren autenticación.
        - El resto de acciones requieren autenticación.
        """
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Endpoint de Registro (No requiere autenticación)
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Hash de la contraseña
            user.save()
            return ApiResponse.success(data={
                'message': f"{self.queryset.model.__name__} registrado correctamente",
            }, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return ApiResponse.error(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Endpoint de Login (No requiere autenticación)
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return ApiResponse.success(data={
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },status=status.HTTP_200_OK)
        return  ApiResponse.error("Credenciales invalidas", status=status.HTTP_400_BAD_REQUEST)

class ConversationViewSet(BaseViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()


class MessageViewSet(BaseViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class ChatbotConfigViewSet(BaseViewSet):
    serializer_class = ChatbotConfigSerializer
    queryset = ChatbotConfig.objects.all()

class ChatLogViewSet(BaseViewSet):
    serializer_class = ChatLogSerializer
    queryset = ChatLog.objects.all()

class TokenViewSet(BaseViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class UploadFileViewSet(BaseViewSet):
    serializer_class = UploadFileSerializer
    queryset = UploadFile.objects.all()