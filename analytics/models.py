from django.db import models
from django.contrib.auth import get_user_model
from tests.models import Test

User = get_user_model()


class Analytics(models.Model):
    """Model to store calculated analytics for each student per test"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    accuracy = models.FloatField(default=0.0)
    correct_incorrect_ratio = models.FloatField(default=0.0)
    avg_time_per_question = models.FloatField(default=0.0)
    change_percentage = models.FloatField(default=0.0)
    revisit_proportion = models.FloatField(default=0.0)
    time_efficiency = models.FloatField(default=0.0)
    behavioral_score = models.FloatField(default=0.0)
    suggestions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics'
        unique_together = ['user', 'test']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} Analytics"


class TestSession(models.Model):
    """Model to track test sessions"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    pause_count = models.IntegerField(default=0)
    total_pause_time = models.FloatField(default=0.0)  # in seconds
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'test_sessions'
        unique_together = ['user', 'test']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} Session"
