from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User

class MyUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyUserSerializer(UserSerializer):
    """Кастомный сериализатор пользователей."""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password')
