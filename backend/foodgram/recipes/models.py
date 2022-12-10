from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(max_length=256, verbose_name='Название')
    color = models.CharField(max_length=16)
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Ключ'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=200, verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единица измерерния')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Игредиент'
        verbose_name_plural = 'Игредиенты'

    def __str__(self) -> str:
        return self.name



class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', verbose_name="Рецепты")
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание рецепта'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='recipes', verbose_name='Теги')
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes', verbose_name='Ингредиенты')
    cooking_time = models.IntegerField()

    class Meta:
        ordering = ['author']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name

class IngredientQuantity(models.Model):
    """Модель описывающая количество ингредиента."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='quantity', verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='quantity', verbose_name='Ингредиент')
    quantity = models.PositiveSmallIntegerField(validators=(MinValueValidator(1, 'Количество ингредиента не можем быть меньше 1'),))

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        
class FavoritesList(models.Model):
    """Модель для списка избранных рецептов."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Избранный рецепт", related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe')
        ]

class CartList(models.Model):
    """Модель описывающая список покупок."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='cart')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe')
        ]
