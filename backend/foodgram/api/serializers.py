import webcolors
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (CartList, Favorite, Ingredient, IngredientQuantity,
                            Recipe, Tag)
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import MyUserSerializer


class Hex2NameColor(serializers.Field):
    """Сериализатор для перевода цвета из hex в имя."""
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


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели IngredientQuantity.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientQuantity.objects.all(),
                fields=['recipe', 'ingredient']
            )
        ]


class AddIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'amount', 'recipe')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра списка рецептов."""
    author = MyUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'tags',
            'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        return IngredientQuantitySerializer(
            IngredientQuantity.objects.filter(recipe=obj),
            many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return CartList.objects.filter(recipe=obj, user=request.user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для публикации рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    author = MyUserSerializer(read_only=True)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'image',
            'author', 'ingredients',
            'name', 'text', 'cooking_time'
        )

    def validate(self, data):
        ingredients = data['ingredients']
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError({
                'ingredients': 'Ингредиенты должны быть уникальными!'
            })
        tags = data['tags']
        if not tags:
            raise ValidationError({
                'tags': 'Вы не выбрали ни одного тега.'
            })
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

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        amount = IngredientQuantity.objects.filter(recipe__id=instance.id)
        amount.delete()
        instance.tags.set(tags)
        self.create_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('tags')
        self.fields.pop('ingredients')
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientQuantitySerializer(
            IngredientQuantity.objects.filter(recipe=instance), many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags, many=True
        ).data
        return representation


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для использования при добавлении рецепта в избранное.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoriteRecipeSerializer(
            instance.recipe, context=context).data


class CartListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    class Meta:
        model = CartList
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoriteRecipeSerializer(
            instance.recipe, context=context).data
