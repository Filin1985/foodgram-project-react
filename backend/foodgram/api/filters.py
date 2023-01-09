from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag, Ingredient
from users.models import User


class CustomRecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)


class IngredientFilter(filters.FilterSet):
    """Фильтр для ингредиентов"""
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ('name', )
