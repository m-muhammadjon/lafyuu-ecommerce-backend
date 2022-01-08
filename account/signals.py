from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Verification
from .views import email_sender


@receiver(post_save, sender=User)
def user_created(sender, instance, **kwargs):
    user = User.objects.get(id=instance.id)
    print(user.email.split('@')[0])
    print("***************************")
    verify, created = Verification.objects.get_or_create(user=user)
    if created:
        email_sender(instance.id)

