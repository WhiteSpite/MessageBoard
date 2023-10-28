from django.db.models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from random import randint


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    subscribed_to_news = BooleanField(default=False)
    subscribed_to_announcements = BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


def get_confirmation_code():
    while True:
        code = str(randint(100000, 999999))
        if not ConfirmationCode.objects.filter(code=code).exists():
            return code


class ConfirmationCode(Model):
    code = CharField(max_length=6, default=get_confirmation_code, unique=True)
    user = ForeignKey(User, on_delete=CASCADE)
    activate_url = URLField()
