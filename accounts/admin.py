from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PreRegisteredStudent, Subject, EmbeddedAnalytics


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    
    list_display = ['username', 'student_id', 'role', 'year_of_study', 'is_approved', 'is_active', 'created_at']
    list_filter = ['role', 'year_of_study', 'is_approved', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'student_id', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Student Information', {
            'fields': ('role', 'student_id', 'year_of_study', 'is_approved', 'approved_by')
        }),
        ('Additional Info', {
            'fields': ('profile_data',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Information', {
            'fields': ('role', 'student_id', 'year_of_study')
        }),
    )


@admin.register(PreRegisteredStudent)
class PreRegisteredStudentAdmin(admin.ModelAdmin):
    """Pre-registered Student Admin"""
    
    list_display = ['student_id', 'full_name', 'year_of_study', 'is_used', 'registered_by', 'created_at']
    list_filter = ['year_of_study', 'is_used', 'registered_by']
    search_fields = ['student_id', 'full_name']
    readonly_fields = ['is_used', 'used_by']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Subject Admin"""
    
    list_display = ['code', 'name', 'teacher', 'year_applicable', 'is_active', 'created_at']
    list_filter = ['year_applicable', 'is_active', 'teacher']
    search_fields = ['name', 'code']


@admin.register(EmbeddedAnalytics)
class EmbeddedAnalyticsAdmin(admin.ModelAdmin):
    """Embedded Analytics Admin"""
    
    list_display = ['name', 'template_type', 'teacher', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active', 'teacher']
    search_fields = ['name', 'teacher__username']
    readonly_fields = ['embed_code', 'last_updated']
