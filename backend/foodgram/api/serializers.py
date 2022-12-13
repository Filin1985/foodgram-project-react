import webcolors
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from users.serializers import MyUserSerializer
from recipes.models import Recipe, Tag, Ingredient


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

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""
    author = MyUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredient = IngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = '__all__'
