from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUserModel, Profile, Task, Province, City
from .forms import AdminPanelUserCreateForm, AdminPanelUserChangeForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'f_name', 'l_name', 'national_code', 'email', 'province', 'city')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('user', 'f_name', 'l_name', 'national_code', 'email', 'province', 'city')


class CustomUserAdmin(BaseUserAdmin):
    form = AdminPanelUserChangeForm
    add_form = AdminPanelUserCreateForm
    inlines = (ProfileInline, )

    list_display = ('phone_number', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'is_verified')}),
        # ('Personal info', {'fields': ('profile', 'is_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(CustomUserModel, CustomUserAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('type', 'code', 'status', 'task_counseling', 'task_session', 'task_visit', 'is_paid', 'datetime_created')
    ordering = ('-datetime_created',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')

