from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import CustomRecipeFilter, IngredientFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthOrReadOnly
from .serializers import (CartListSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          RecipeSerializer, TagSerializer)
from .utils import post_favorite_cart, delete_favorite_cart
from recipes.models import (
    CartList,
    Favorite,
    Ingredient,
    IngredientQuantity,
    Recipe,
    Tag
)


class TagViewSet(ReadOnlyModelViewSet):
    """
    Endpoint для получения списка тэгов и тэга по id.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Endpoint для получения списка ингредиентов и ингредиента по id.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """
    Endpoint для получения, создания, изменения, удаления рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = CustomRecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientQuantity.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            qty=Sum('amount')
        ).order_by()
        data = []
        data.append('список покупок')
        data.append('ингридиент, ед. - количество')
        text = 'Список покупок:\n\n'
        for _, ingredient in enumerate(ingredients, 1):
            text += (
                f'{ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' — {ingredient["qty"]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class FavoriteApiView(APIView):
    """
    Endpoint для создания и удаления избранных рецептов.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        return post_favorite_cart(FavoriteSerializer, request, id)

    def delete(self, request, id):
        return delete_favorite_cart(request, id, Favorite, Recipe)


class CartListApiView(APIView):
    """
    Endpoint для создания и удаления списка покупок.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        return post_favorite_cart(CartListSerializer, request, id)

    def delete(self, request, id):
        return delete_favorite_cart(request, id, CartList, Recipe)
