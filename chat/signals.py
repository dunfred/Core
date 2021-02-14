from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chat.models import Profile

@receiver(post_save, sender=User)
def create_new_user_profile(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    print('created', created)
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()



