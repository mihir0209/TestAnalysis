from django.db import models
from django.contrib.auth import get_user_model
import string
import random

User = get_user_model()


class Room(models.Model):
    """Room model for managing test sessions"""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    invite_code = models.CharField(max_length=10, unique=True, blank=True)
    entry_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_students = models.IntegerField(default=50)
    late_penalty = models.FloatField(default=1.0, help_text="Penalty marks for late entry")
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rooms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.teacher.username}"
    
    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)
    
    def generate_invite_code(self):
        """Generate unique invite code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Room.objects.filter(invite_code=code).exists():
                return code
    
    @property
    def current_students_count(self):
        return self.participants.count()
    
    @property
    def is_full(self):
        return self.current_students_count >= self.max_students


class RoomParticipant(models.Model):
    """Model to track room participants"""
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)
    penalty_applied = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'room_participants'
        unique_together = ['room', 'student']
    
    def __str__(self):
        return f"{self.student.username} in {self.room.name}"
