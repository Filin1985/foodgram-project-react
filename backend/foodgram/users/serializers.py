from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User

class MyUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password')

class MyUserSerializer(UserSerializer):
    """Кастомный сериализатор пользователей."""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password')
