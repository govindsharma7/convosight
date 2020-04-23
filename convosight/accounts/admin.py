from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from convosight.accounts.models import User


# Register your models here.
class UserAdmin(AuthUserAdmin):
    """
    Here we list all the fields we need
    to see in the admin pannel of django admin
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {'fields': ('user_type', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    list_display = (
        'email', 'first_name', 'last_name', 'is_active'
    )
    list_editable = ('is_active',)
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')


admin.site.register(User, UserAdmin)
