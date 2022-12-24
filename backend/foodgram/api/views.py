from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (CartList, Favorite, Ingredient, IngredientQuantity,
                            Recipe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import CustomRecipeFilter
from .pagination import MyPageNumberPagination
from .permissions import IsAuthOrReadOnly
from .serializers import (CartListSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          RecipeSerializer, TagSerializer)


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
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="список_покупок.pdf"')
        page = canvas.Canvas(response)
        pdfmetrics.registerFont(
            TTFont('Roboto', '../../data/roboto.ttf', 'UTF-8'))
        page.setFont('Roboto', size=24)
        page.drawString(140, 800, 'Список необходимых покупок')
        page.setFont('Roboto', size=14)
        height = 750
        ingredients = IngredientQuantity.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        product_list = {}
        for ingredient in ingredients:
            name = ingredient[0]
            if name not in product_list:
                product_list[name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                product_list[name]['amount'] += ingredient[2]
        for i, (name, data) in enumerate(product_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response


class FavoriteApiView(APIView):
    """
    Endpoint для создания и удаления избранных рецептов.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        serializer = FavoriteSerializer(data={
            'recipe': id,
            'user': request.user.id
        }, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartListApiView(APIView):
    """
    Endpoint для создания и удаления списка покупок.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        serializer = CartListSerializer(data={
            'recipe': id,
            'user': request.user.id
        }, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        CartList.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
