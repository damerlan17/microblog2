from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models  import User
from .models import Profile

# Создаём профиль при создании пользователя
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Удаляем пользователя при удалении профиля (опционально)
@receiver(post_delete, sender=Profile)
def delete_user_with_profile(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()