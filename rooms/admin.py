from django.contrib import admin
from .models import Room, RoomParticipant


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin"""
    
    list_display = ['name', 'teacher', 'invite_code', 'is_active', 'current_students_count', 'max_students', 'created_at']
    list_filter = ['is_active', 'created_at', 'teacher']
    search_fields = ['name', 'invite_code', 'teacher__username']
    readonly_fields = ['invite_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'teacher')
        }),
        ('Room Settings', {
            'fields': ('invite_code', 'entry_deadline', 'is_active', 'max_students', 'late_penalty')
        }),
        ('Advanced Settings', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoomParticipant)
class RoomParticipantAdmin(admin.ModelAdmin):
    """Room Participant Admin"""
    
    list_display = ['room', 'student', 'joined_at', 'is_late', 'penalty_applied']
    list_filter = ['is_late', 'joined_at', 'room']
    search_fields = ['room__name', 'student__username']
