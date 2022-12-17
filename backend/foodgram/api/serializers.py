import webcolors
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import MyUserSerializer
from recipes.models import User, Recipe, Tag, Ingredient, IngredientQuantity, FavoritesList, CartList


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    color = Hex2NameColor()
    
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',

class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientQuantity."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientQuantity
        fields = '__all__'

class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра списка рецептов."""
    author = MyUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        return IngredientQuantitySerializer(IngredientQuantity.objects.filter(recipe=obj), many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoritesList.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return CartList.objects.filter(recipe=obj, user=request.user).exists()

    

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для публикации рецепта."""
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = AddIngredientSerializer(many=True)
    author = MyUserSerializer(read_only=True)
    image = Base64ImageField()
    

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'image', 'author', 'ingredients', 'name', 'text', 'cooking_time')

    def validate(self, data):
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    

class FavoritesListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FavoritesList."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = FavoritesList
        fields = '__all__'
        extra_kwargs = {'following': {'required': True}}
        validators = [
            UniqueTogetherValidator(
                queryset=FavoritesList.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise ValidationError("Автор не может подписаться на самого себя")
        return value