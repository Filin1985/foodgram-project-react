from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели  Recipe."""
    list_display = ('name', 'author', 'favorite_count')
    list_filter = ('name', 'author', 'tags')

    def favorite_count(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Ingredient."""
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
