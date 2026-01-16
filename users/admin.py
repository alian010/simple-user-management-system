"""
Django Admin Configuration for Custom User Model
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin for email-based authentication
    """
    
    # Display configuration
    list_display = ['email', 'full_name', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'full_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    # Fieldsets for edit page
    fieldsets = (
        ('Login Credentials', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('full_name',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )
    
    # Fieldsets for add page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )
    
    # Optimize database queries
    def get_queryset(self, request):
        """Optimize queries with prefetch"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups', 'user_permissions')