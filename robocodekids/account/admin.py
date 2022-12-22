from django.contrib import admin
from .models import User
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "username")
    search_fields = ("username", "bio", "created_at")

    def user_image(self, obj):
        return format_html('<img src="{}" width="100px" height="100px" />'.format(obj.avatar.url))

    list_display = ['user_image', 'username', 'created_at']
