from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.mail import send_mail  
from django.conf import settings  
User = get_user_model()

@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        # Уведомление о регистрации нового пользователя
        subject = "Добро пожаловать на платформу!"
        message = f"Здравствуйте, {instance.username}! Спасибо за регистрацию."
        recipient_list = [instance.email]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
