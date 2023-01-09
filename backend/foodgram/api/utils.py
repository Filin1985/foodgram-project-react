from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def post_favorite_cart(input_serializer, request, id):
    print(id)
    print(request['context'])
    serializer = input_serializer(data={
        'recipe': id,
        'user': request.user.id
    }, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_favorite_cart(request, id, input_model, recipe_model):
    recipe = get_object_or_404(recipe_model, id=id)
    input_model.objects.filter(user=request.user, recipe=recipe).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
