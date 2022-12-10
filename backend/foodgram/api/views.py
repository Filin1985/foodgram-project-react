from django.shortcuts import render
from rest_framework import viewsets, mixins, filters
from .serializers import RecipeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import Recipe, Tag

class RecipeViewSet(viewsets.ModelViewSet):
    """
    Endpoint для получения, создания, изменения, удаления рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)