from django.contrib import admin

from .models import Post, Group, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'text',
        'pub_date', 'group',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text', 'post',
    )


@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug', 'description',
    )
