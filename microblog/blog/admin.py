# blog/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Отменяем регистрацию стандартного User и регистрируем с профилем
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_on', 'likes_count', 'comments_count')
    list_filter = ('created_on', 'author')
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created_on'

    @admin.display(description='Текст (предв.)')
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    def likes_count(self, obj):
        return obj.like_set.count()
    likes_count.short_description = 'Лайков'

    def comments_count(self, obj):
        return obj.comment_set.count()
    comments_count.short_description = 'Комментариев'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_preview', 'content_preview', 'created_on')
    list_filter = ('created_on', 'author')
    search_fields = ('content', 'author__username', 'post__content')

    def post_preview(self, obj):
        return obj.post.content[:30] + '...'
    post_preview.short_description = 'Пост'

    def content_preview(self, obj):
        return obj.content[:40] + '...'
    content_preview.short_description = 'Комментарий'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'created_on')
    list_filter = ('created_on', 'user')
    search_fields = ('user__username',)

    def post_preview(self, obj):
        return obj.post.content[:30] + '...'
    post_preview.short_description = 'Пост'