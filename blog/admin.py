from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'views', 'created_at', 'owner')
    list_filter = ('title', 'created_at')
    search_fields = ('title', 'created_at')
