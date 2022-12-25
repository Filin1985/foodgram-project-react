from django.shortcuts import get_object_or_404


def bulk_create(ingredients_data, models, recipe):
    bulk_create_data = (
        models(
            recipe=recipe,
            ingredient=ingredient_data['ingredient'],
            amount=ingredient_data['amount'])
        for ingredient_data in ingredients_data
    )
    models.objects.bulk_create(bulk_create_data)


def post_favorite_cart(input_serializer, request, id):
    serializer = input_serializer(data={
        'recipe': id,
        'user': request.user.id
    }, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


def delete_favorite_cart(request, id, input_model, recipe_model):
    recipe = get_object_or_404(recipe_model, id=id)
    input_model.objects.filter(user=request.user, recipe=recipe).delete()
