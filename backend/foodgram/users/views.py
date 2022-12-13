from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny

from api.permissions import IsAdminOrReadOnly
from .models import User
from .serializers import MyUserCreateSerializer, MyUserSerializer


class MyUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = MyUserSerializer


