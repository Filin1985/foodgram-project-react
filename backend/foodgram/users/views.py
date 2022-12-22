from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.pagination import MyPageNumberPagination
from .models import User, Follow
from .serializers import FollowSerializer, MyUserSerializer


class MyUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPageNumberPagination

    @action(methods=['POST', 'DELETE'], permission_classes=[IsAuthenticated], detail=True)
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user == author:
                return Response({
                    'errors': 'Вы не можете подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=request.user, author=author).exists():
                return Response({
                    'errors': f'Вы уже подписаны на {author}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follower = Follow.objects.create(user=request.user, author=author)
            serializer = FollowSerializer(follower, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if Follow.objects.filter(user=request.user, author=author).exists():
            follower = get_object_or_404(Follow, user=request.user, author=author)
            follower.delete()
            return Response({
                    f'Вы больше не подписаны на {author}'},
                    status=status.HTTP_204_NO_CONTENT
                )

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        following = Follow.objects.filter(user=request.user)
        print(following)
        return Response(
            {'errors': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )