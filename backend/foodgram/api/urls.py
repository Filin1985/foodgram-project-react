from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
# router.register('ingredients', RecipeViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls))
]
