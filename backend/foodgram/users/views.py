from api.pagination import CustomPageNumberPagination
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, CustomUserSerializer


class MyUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination

    @action(
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated], detail=True
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user == author:
                return Response({
                    'errors': 'Вы не можете подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(
                user=request.user,
                author=author
            ).exists():
                return Response({
                    'errors': f'Вы уже подписаны на {author}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follower = Follow.objects.create(user=request.user, author=author)
            serializer = FollowSerializer(
                follower, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Follow.objects.filter(user=request.user, author=author).exists()
        follower = get_object_or_404(Follow, user=request.user, author=author)
        follower.delete()
        return Response({
                    f'Вы больше не подписаны на {author}'},
                    status=status.HTTP_204_NO_CONTENT
                )

    @action(
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        detail=False
    )
    def subscriptions(self, request):
        serializer = FollowSerializer(
            self.paginate_queryset(
                Follow.objects.filter(user=request.user)
            ),
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
