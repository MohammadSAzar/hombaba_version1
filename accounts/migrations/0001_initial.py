# Generated by Django 5.0.4 on 2024-12-26 11:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('otp_code', models.PositiveIntegerField(blank=True, null=True)),
                ('otp_code_datetime_created', models.DateTimeField(auto_now=True)),
                ('is_verified', models.CharField(blank=True, choices=[('a', 'Authenticated'), ('n', 'Not Authenticated'), ('i', 'In Progress')], default='n', max_length=10, null=True, verbose_name='Authentication Status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='First Name')),
                ('l_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Last Name')),
                ('sex', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=10, null=True, verbose_name='Sex')),
                ('national_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='National Code')),
                ('email', models.CharField(blank=True, max_length=300, null=True, verbose_name='ایمیل')),
                ('province', models.CharField(blank=True, max_length=150, null=True, verbose_name='Province')),
                ('city', models.CharField(blank=True, max_length=150, null=True, verbose_name='City')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Address')),
                ('introduction_way', models.CharField(blank=True, choices=[('ins', 'Instagram'), ('y&a', 'Course Videos'), ('ads', 'Advertisements'), ('web', 'Website and Google'), ('frd', 'Friends'), ('oth', 'Others')], max_length=10, null=True, verbose_name='Introduction Way')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='accounts.province')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('cns', 'Counseling'), ('ses', 'Session'), ('vis', 'Visit')], max_length=6, null=True, verbose_name='Task Type')),
                ('is_paid', models.CharField(blank=True, choices=[('yes', 'بله'), ('no', 'خیر')], default='no', max_length=10, null=True, verbose_name='Payment Status')),
                ('status', models.CharField(blank=True, choices=[('tkn', 'Taken'), ('fre', 'Free'), ('pen', 'Pending')], default='fre', max_length=10, null=True, verbose_name='Request Status')),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time of Creation')),
                ('task_counseling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counseling_task', to='services.counseling')),
                ('task_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='session_task', to='services.session')),
                ('task_visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visit_task', to='services.visit')),
            ],
            options={
                'ordering': ('-datetime_created',),
            },
        ),
    ]
