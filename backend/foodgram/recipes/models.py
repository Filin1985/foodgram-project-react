from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from foodgram.settings import RECIPE_MAX_LENGTH
from users.models import User


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Название'
    )
    color = ColorField(
        unique=True,
        max_length=7,
        verbose_name='Цвет в HEX',
        blank=True,
        null=True,
        default='#FFFFE0'
    )
    slug = models.SlugField(
        max_length=RECIPE_MAX_LENGTH,
        unique=True,
        verbose_name='Уникальный ключ')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=RECIPE_MAX_LENGTH,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=RECIPE_MAX_LENGTH,
        verbose_name='Единица измерерния'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Игредиент'
        verbose_name_plural = 'Игредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=RECIPE_MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/', null=True,
        blank=True, verbose_name='Изображение'
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание рецепта'
    )
    tags = models.ManyToManyField(
        'Tag', blank=True,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        'Ingredient', through='IngredientQuantity',
        related_name='recipes', verbose_name='Ингредиенты',
        validators=(MinValueValidator(
            1, message='Минимальное количество ингредиента - 1'),
        ))

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        ))

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_author_name')
        ]

    def __str__(self) -> str:
        return self.name


class IngredientQuantity(models.Model):
    """Модель описывающая количество ингредиента."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='amount', verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='amount', verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, 'Количество ингредиента не можем быть меньше 1'
            ),
        )
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_recipe_ingredient')
        ]


class Favorite(models.Model):
    """Модель для списка избранных рецептов."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name="Избранный рецепт", related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe')
        ]

    def __str__(self):
        return f'{self.recipe} в избраннои у пользователя {self.user}'


class CartList(models.Model):
    """Модель описывающая список покупок."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт', related_name='cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart recipe')
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
