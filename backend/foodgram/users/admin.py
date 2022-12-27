from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели User."""
    list_filter = ('username', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
