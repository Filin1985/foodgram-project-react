import webcolors
from rest_framework import serializers

from djoser.serializers import UserSerializer
from users.models import User
from recipes.models import Recipe


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', id, 'username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    class Meta:
        fields = '__all__'
        model = Recipe