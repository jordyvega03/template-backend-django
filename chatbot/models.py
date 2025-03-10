from django.contrib.auth.models import AbstractUser
from django.db import models

# 🔹 1. Modelo de Usuario
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="chatbot_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="chatbot_users_permissions",
        blank=True
    )

    def __str__(self):
        return self.username


# 🔹 2. Modelo de Conversaciones
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación {self.id} - {self.user.username}"


# 🔹 3. Modelo de Mensajes
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    message = models.TextField()
    response = models.TextField(blank=True, null=True)  # Respuesta del bot (opcional)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} ({self.timestamp}): {self.message[:50]}"


# 🔹 4. Modelo de Configuración del Chatbot
class ChatbotConfig(models.Model):
    parameter = models.CharField(max_length=50, unique=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.parameter}: {self.value}"


# 🔹 5. Modelo de Logs de Interacción
class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True)
    input_text = models.TextField()
    generated_text = models.TextField()
    response_time = models.FloatField()  # Tiempo en milisegundos
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id} - {self.timestamp}"


# 🔹 6. Modelo de Tokens (para autenticación JWT si lo necesitas)
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token de {self.user.username}"


# 🔹 7. Modelo de Archivos Adjuntos en el Chat (si el chatbot soporta archivos)
class UploadFile(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="uploads")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploads")
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo de {self.user.username} - {self.file.name}"