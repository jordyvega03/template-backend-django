from chatbot.models import User, ChatLog, Conversation, Message, ChatbotConfig, Token, UploadFile
from rest_framework import serializers
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatbotConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotConfig
        fields = '__all__'

class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'

class ApiResponse:
    @staticmethod
    def success(data=None, message="Operación exitosa", status=200):
        return Response({
            "status": status,
            "message": message,
            "data": data
        }, status=status)

    @staticmethod
    def error(errors=None, message="Error en la solicitud", status=400):
        return Response({
            "status": status,
            "message": message,
            "errors": errors if errors else []
        }, status=status)