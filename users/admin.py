from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'token')
    list_filter = ('email', 'first_name', 'last_name', 'phone')
    search_fields = ('email',)
