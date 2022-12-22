from rest_framework import mixins, filters
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .serializers import RecipeListSerializer, TagSerializer, IngredientSerializer, RecipeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from recipes.models import Recipe, Tag, Ingredient
from .permissions import IsAdminOrReadOnly, IsAuthOrReadOnly
from .pagination import MyPageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    """
    Endpoint для получения списка тэгов и тэга по id.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def get_paginated_response(self, data):
       return Response(data)


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Endpoint для получения списка ингредиентов и ингредиента по id.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer

    def get_paginated_response(self, data):
       return Response(data)


class RecipeViewSet(ModelViewSet):
    """
    Endpoint для получения, создания, изменения, удаления рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthOrReadOnly,)
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
