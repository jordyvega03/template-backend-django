from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chatbot import views
from .views import ProtectedView, UserViewSet

version = "v1"

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path(f"api/{version}/", include(router.urls)),
    path("protected/", ProtectedView.as_view(), name="protected"),
]