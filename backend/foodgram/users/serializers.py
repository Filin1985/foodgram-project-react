from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow, User


class MyUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = (
            'id', 'email',
            'first_name', 'last_name',
            'username', 'password'
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserSerializer(UserSerializer):
    """Кастомный сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name',
            'last_name', 'username', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    """
    Вспомогательный сериализатор для сохранения рецепта в избранное.
    """
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Follow
        fields = (
            'email', 'username',
            'last_name', 'first_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        return FollowRecipeSerializer(queryset, many=True).data
