import random
import string

from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from jdatetime import date, timedelta, datetime

from . import choices


# --------------------------------- Needs ---------------------------------
def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=10))


def next_seven_days_shamsi():
    days = []
    today = datetime.today()
    for i in range(1, 8):
        next_day = today + timedelta(days=i)
        weekday_en = next_day.strftime('%A')
        date_str = next_day.strftime('%Y/%m/%d')
        weekday_fa = {
            'Monday': 'دوشنبه',
            'Tuesday': 'سه‌شنبه',
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنج‌شنبه',
            'Friday': 'جمعه',
            'Saturday': 'شنبه',
            'Sunday': 'یکشنبه',
        }.get(weekday_en, weekday_en)
        label = f"{weekday_fa} - {date_str}"
        days.append((date_str, label))
    return days


# --------------------------------- Locations ---------------------------------
class Province(models.Model):
    name = models.CharField(max_length=100)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Date and Time of Creation'))

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Date and Time of Creation'))

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

    def __str__(self):
        return self.name


class District(models.Model):
    name_code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Humanized Name'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')
    price_session_sale = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Sale Session Price'))
    price_visit_sale = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Sale Visit Price'))
    price_session_rent = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Rent Session Price'))
    price_visit_rent = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Rent Visit Price'))
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if int(self.name_code):
            i = int(self.name_code)
            if len(self.name_code) == 1:
                self.name_code = '0' + self.name_code
            self.price_session_sale = int(1000000*choices.price_session_sales[i-1][1])
            self.price_visit_sale = int(1000000*choices.price_visit_sales[i-1][1])
            self.price_session_rent = int(1000000*choices.price_session_rents[i-1][1])
            self.price_visit_rent = int(1000000*choices.price_visit_rents[i-1][1])
        super(District, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name_code']
        verbose_name = 'محله (منطقه)'
        verbose_name_plural = 'محلات (مناطق)'

    def __str__(self):
        return self.name


# --------------------------------- Services ---------------------------------
class Counseling(models.Model):
    # Fields
    city = models.CharField(max_length=30, choices=choices.counseling_cities, blank=True, null=True, verbose_name=_('City'))
    counseling_type = models.CharField(max_length=30, default='oc', choices=choices.counseling_types, verbose_name=_('Counseling Type'))
    date = models.CharField(max_length=200, verbose_name=_('Date of Counseling'))
    time = models.CharField(max_length=200, choices=choices.times, verbose_name=_('Time of Counseling'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    code = models.CharField(max_length=12, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        if self.counseling_type != 'ip':
            self.city = None
        super(Counseling, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'مشاوره'
        verbose_name_plural = 'مشاوره‌ها'

    @property
    def price(self):
        price = choices.price_counseling
        return price

    @property
    def tax(self):
        tax = int(choices.price_counseling * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(choices.price_counseling + choices.price_counseling * 0.1)
        return price_plus_tax

    def get_absolute_url(self):
        return reverse('counseling_detail', args=[self.pk, self.code])


class Session(models.Model):
    # Locations
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, default='تهران', null=True, blank=True, related_name='sessions', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name=_('District'))
    # Fields
    customer_type = models.CharField(max_length=10, choices=choices.customer_types, verbose_name=_('Customer Type'))
    trade_type = models.CharField(max_length=10, blank=True, null=True, choices=choices.trade_types, verbose_name=_('Trade Type'))
    date = models.CharField(max_length=200, verbose_name=_('Date of Session'))
    time = models.CharField(max_length=200, choices=choices.times, verbose_name=_('Time of Session'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    code = models.CharField(max_length=12, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super(Session, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'نشست'
        verbose_name_plural = 'نشست‌ها'

    @property
    def price(self):
        if self.trade_type == 'rt':
            price = self.district.price_session_rent
        else:
            price = self.district.price_session_sale
        return price

    @property
    def tax(self):
        tax = int(self.price * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(self.price + self.tax)
        return price_plus_tax

    def get_absolute_url(self):
        return reverse('session_detail', args=[self.pk, self.code])


class Visit(models.Model):
    # Locations
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, default='تهران', null=True, blank=True, related_name='visits', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name=_('District'))
    # Fields
    trade_type = models.CharField(max_length=10, blank=True, null=True, choices=choices.trade_types, verbose_name=_('Trade Type'))
    date = models.CharField(max_length=200, verbose_name=_('Date of Visit'))
    time = models.CharField(max_length=200, choices=choices.times, verbose_name=_('Time of Visit'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    code = models.CharField(max_length=12, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super(Visit, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدیدها'

    @property
    def price(self):
        if self.trade_type == 'st':
            price = self.district.price_visit_sale
        else:
            price = self.district.price_visit_rent
        return price

    @property
    def tax(self):
        tax = int(self.price * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(self.price + self.tax)
        return price_plus_tax

    def get_absolute_url(self):
        return reverse('visit_detail', args=[self.pk, self.code])




