# Generated by Django 5.0.4 on 2025-06-05 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_remove_visit_customer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='نام محله (منطقه)'),
        ),
        migrations.AlterField(
            model_name='district',
            name='price_session_rent',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت نشست رهن و اجاره'),
        ),
        migrations.AlterField(
            model_name='district',
            name='price_session_sale',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت نشست خرید و فروش'),
        ),
        migrations.AlterField(
            model_name='district',
            name='price_visit_rent',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت بازدید رهن و اجاره'),
        ),
        migrations.AlterField(
            model_name='district',
            name='price_visit_sale',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت بازدید فروش'),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.CharField(max_length=200, verbose_name='تاریخ نشست'),
        ),
        migrations.AlterField(
            model_name='session',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions', to='services.district', verbose_name='محله (منطقه)'),
        ),
        migrations.AlterField(
            model_name='session',
            name='time',
            field=models.CharField(choices=[('mg', 'صبح'), ('nn', 'ظهر'), ('eg', 'عصر'), ('nt', 'شب')], max_length=200, verbose_name='زمان نشست'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='services.district', verbose_name='محله (منطقه)'),
        ),
    ]
