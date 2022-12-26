from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CartListApiView,
    FavoriteApiView,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteApiView.as_view(), name='favorites'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        CartListApiView.as_view(), name='cart'
    ),
]
