from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Factory
from .tasks import run_factory


@receiver(post_save, sender=Factory)
def my_handler(sender, instance, **kwargs):
    run_factory.delay(instance.pk)