from django.shortcuts import render
from rest_framework import viewsets, mixins, filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from recipes.models import Recipe, Tag, Ingredient
from .permissions import IsAdminOrReadOnly
from .pagination import MyPageNumberPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint для получения списка тэгов и тэга по id.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def get_paginated_response(self, data):
       return Response(data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint для получения списка ингредиентов и ингредиента по id.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer

    def get_paginated_response(self, data):
       return Response(data)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Endpoint для получения, создания, изменения, удаления рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RecipeSerializer
    pagination_class = MyPageNumberPagination 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


