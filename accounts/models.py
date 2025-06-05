import random
import string

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import CustomUserManager
from services.models import Counseling, Session, Visit
from . import choices


# --------------------------------- Locations ---------------------------------
class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

    def __str__(self):
        return self.name


# --------------------------------- User ---------------------------------
class CustomUserModel(AbstractUser):
    IS_VERIFIED_CHOICES = [
        ('a', _('Authenticated')),
        ('n', _('Not Authenticated')),
        ('i', _('In Progress')),
    ]
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    otp_code = models.PositiveIntegerField(blank=True, null=True)
    otp_code_datetime_created = models.DateTimeField(auto_now=True)
    is_verified = models.CharField(max_length=10, choices=IS_VERIFIED_CHOICES, blank=True, null=True, default='n', verbose_name=_('Authentication Status'))

    objects = CustomUserManager()
    backend = 'accounts.backends.CustomAuthBackend'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    # Fields
    f_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('First Name'))
    l_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('Last Name'))
    sex = models.CharField(max_length=10, choices=choices.sexes, blank=True, null=True, verbose_name=_('Sex'))
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    province = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Province'))
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('City'))
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))
    introduction_way = models.CharField(max_length=10, choices=choices.ways, blank=True, null=True, verbose_name=_('Introduction Way'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'


# --------------------------------- Tasks ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=10))


class Task(models.Model):
    task_counseling = models.ForeignKey(Counseling, on_delete=models.CASCADE, related_name='counseling_task', blank=True, null=True)
    task_session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_task', blank=True, null=True)
    task_visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visit_task', blank=True, null=True)
    type = models.CharField(max_length=6, choices=choices.task_types, null=True, blank=True, verbose_name=_('Task Type'))
    is_paid = models.CharField(max_length=10, choices=choices.payment_statuses, blank=True, null=True, default='no', verbose_name=_('Payment Status'))
    status = models.CharField(max_length=10, choices=choices.statuses, blank=True, null=True, default='fre', verbose_name=_('Request Status'))
    code = models.CharField(max_length=10, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} / {self.type}'

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = 'وظیفه'
        verbose_name_plural = 'وظایف'



