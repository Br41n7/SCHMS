"""
Admin configuration for User model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    """
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('middle_name', 'phone_number', 'profile_completed')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'phone_number')
        }),
    )