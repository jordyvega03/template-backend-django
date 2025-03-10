from django.contrib import admin

from .models import User, Conversation, Message, ChatbotConfig, ChatLog, Token, UploadFile

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ChatbotConfig)
admin.site.register(ChatLog)
admin.site.register(Token)
admin.site.register(UploadFile)
