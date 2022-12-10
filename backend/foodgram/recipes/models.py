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
    ingredient = models.ManyToManyField('Ingredient', related_name='recipes', verbose_name='Ингредиенты')
    cooking_time = models.IntegerField()

    class Meta:
        ordering = ['author']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name
