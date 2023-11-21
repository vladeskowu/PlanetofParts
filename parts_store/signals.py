from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Cart

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:

        if not hasattr(instance, 'userprofile'):
            UserProfile.objects.create(user=instance)

        Cart.objects.get_or_create(user_profile=instance.userprofile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=UserProfile)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user_profile=instance)

@receiver(post_save, sender=UserProfile)
def save_user_cart(sender, instance, **kwargs):
    try:
        instance.cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user_profile=instance)
