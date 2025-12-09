
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile, Post, Comment, Like


# Инлайн для профиля внутри пользователя
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Профиль"
    verbose_name_plural = "Профили"
    readonly_fields = ('avatar_preview',)
    fields = ('avatar', 'avatar_preview', 'bio')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%;" />', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Аватар (превью)"


# Расширяем стандартную админку User
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Перерегистрируем User с профилем
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Админка для постов
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_on', 'likes_count', 'comments_count')
    list_filter = ('created_on', 'author')
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created_on'
    readonly_fields = ('created_on', 'updated_on')

    @admin.display(description="Текст поста")
    def content_preview(self, obj):
        return (obj.content[:70] + '…') if len(obj.content) > 70 else obj.content

    def likes_count(self, obj):
        return obj.like_set.count()
    likes_count.short_description = "Лайков"

    def comments_count(self, obj):
        return obj.comment_set.count()
    comments_count.short_description = "Комментариев"


# Админка для комментариев
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_preview', 'content_preview', 'created_on')
    list_filter = ('created_on', 'author')
    search_fields = ('content', 'author__username', 'post__content')
    readonly_fields = ('created_on', 'updated_on')

    @admin.display(description="Пост")
    def post_preview(self, obj):
        return (obj.post.content[:50] + '…') if len(obj.post.content) > 50 else obj.post.content

    @admin.display(description="Комментарий")
    def content_preview(self, obj):
        return (obj.content[:60] + '…') if len(obj.content) > 60 else obj.content


# Админка для лайков
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'created_on')
    list_filter = ('created_on', 'user')
    search_fields = ('user__username', 'post__content')

    @admin.display(description="Пост")
    def post_preview(self, obj):
        return (obj.post.content[:50] + '…') if len(obj.post.content) > 50 else obj.post.content