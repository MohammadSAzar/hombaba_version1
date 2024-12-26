from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from services.models import Counseling, Session, Visit


@receiver(post_save, sender=Counseling)
def task_counseling_signal(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_counseling=instance, type='cns')


@receiver(post_save, sender=Session)
def task_session_signal(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_session=instance, type='ses')


@receiver(post_save, sender=Visit)
def task_visit_signal(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(task_visit=instance, type='vis')



