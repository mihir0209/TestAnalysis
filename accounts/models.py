from django.contrib.auth.models import AbstractUser
from django.db import models
import re


class User(AbstractUser):
    """Custom User model with role-based authentication"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    YEAR_CHOICES = [
        ('FY', 'First Year'),
        ('SY', 'Second Year'),
        ('TY', 'Third Year'),
        ('LY', 'Last Year'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    year_of_study = models.CharField(max_length=2, choices=YEAR_CHOICES, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_students')
    profile_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        if self.student_id:
            return f"{self.student_id} - {self.get_full_name()}"
        return f"{self.username} ({self.role})"
    
    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def validate_student_id(self):
        """Validate student ID format (e.g., TY-4789)"""
        if self.student_id:
            pattern = r'^(FY|SY|TY|LY)-\d{4}$'
            return re.match(pattern, self.student_id) is not None
        return False
    
    def save(self, *args, **kwargs):
        # Auto-approve teachers and admins
        if self.role in ['teacher', 'admin']:
            self.is_approved = True
        super().save(*args, **kwargs)


class PreRegisteredStudent(models.Model):
    """Model to store pre-registered student IDs by teachers"""
    
    student_id = models.CharField(max_length=20, unique=True)
    year_of_study = models.CharField(max_length=2, choices=User.YEAR_CHOICES)
    full_name = models.CharField(max_length=100)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_students')
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_registrations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'pre_registered_students'
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class Subject(models.Model):
    """Model for subjects taught by teachers"""
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    year_applicable = models.CharField(max_length=2, choices=User.YEAR_CHOICES)
    is_active = models.BooleanField(default=True)
    archived_data = models.JSONField(default=dict, blank=True)  # For saving course data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subjects'
        unique_together = ['teacher', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class EmbeddedAnalytics(models.Model):
    """Model for embeddable analytics widgets"""
    
    TEMPLATE_CHOICES = [
        ('student_performance', 'Student Performance'),
        ('test_performance', 'Test Performance'),
        ('live_results', 'Live Results'),
        ('class_overview', 'Class Overview'),
        ('behavioral_insights', 'Behavioral Insights'),
    ]
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_CHOICES)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='embedded_widgets')
    embed_code = models.TextField(blank=True)
    embed_password = models.CharField(max_length=100)
    settings = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'embedded_analytics'
    
    def __str__(self):
        return f"{self.name} - {self.template_type}"
    
    def generate_embed_code(self):
        """Generate HTML embed code"""
        base_url = "http://localhost:8000"  # Will be dynamic in production
        embed_html = f"""
        <iframe 
            src="{base_url}/embed/{self.id}/" 
            width="100%" 
            height="400" 
            frameborder="0"
            style="border: 1px solid #ddd; border-radius: 8px;">
        </iframe>
        """
        self.embed_code = embed_html
        self.save()
        return embed_html
