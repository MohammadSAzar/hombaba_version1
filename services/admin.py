from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Counseling, Session, Visit
from accounts.models import Task


@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    list_display = ('counseling_type', 'status', 'task_link', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created',)
    ordering = ('-datetime_created', )

    def status(self, obj):
        counseling_task = Task.objects.filter(task_counseling=obj).first()
        if counseling_task:
            return counseling_task.status
    status.short_description = 'status'

    def task_link(self, obj):
        task = Task.objects.filter(task_counseling=obj).first()
        if task:
            url = reverse("admin:accounts_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'status', 'task_link', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created')
    ordering = ('-datetime_created', )

    def status(self, obj):
        session_task = Task.objects.filter(task_session=obj).first()
        if session_task:
            return session_task.status
    status.short_description = 'status'

    def task_link(self, obj):
        task = Task.objects.filter(task_session=obj).first()
        if task:
            url = reverse("admin:accounts_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'status', 'task_link', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created')
    ordering = ('-datetime_created', )

    def status(self, obj):
        visit_task = Task.objects.filter(task_visit=obj).first()
        if visit_task:
            return visit_task.status
    status.short_description = 'status'

    def task_link(self, obj):
        task = Task.objects.filter(task_visit=obj).first()
        if task:
            url = reverse("admin:accounts_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


