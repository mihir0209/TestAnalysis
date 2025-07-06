from django.db import models
from django.contrib.auth import get_user_model
from rooms.models import Room

User = get_user_model()


class Test(models.Model):
    """Test model for managing assessments"""
    
    ANALYTICS_MODES = [
        ('realtime', 'Real-time'),
        ('batch', 'Batch Processing'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='test', null=True, blank=True)
    can_pause = models.BooleanField(default=False)
    analytics_mode = models.CharField(max_length=20, choices=ANALYTICS_MODES, default='batch')
    total_time = models.IntegerField(help_text="Total time in minutes")
    questions_count = models.IntegerField(default=0)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.created_by.username}"


class Question(models.Model):
    """Question model for test questions"""
    
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('theory', 'Theory'),
    ]
    
    EVALUATION_TYPES = [
        ('exact', 'Exact Match'),
        ('keyword', 'Keyword Based'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.JSONField(default=list, blank=True)  # For MCQ options
    correct_answer = models.TextField()
    evaluation_type = models.CharField(max_length=20, choices=EVALUATION_TYPES, default='exact')
    keywords = models.JSONField(default=dict, blank=True)  # For keyword-based evaluation
    keyword_threshold = models.FloatField(default=0.7)
    difficulty_level = models.CharField(max_length=20, default='medium')
    marks = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['id']
    
    def __str__(self):
        return f"Q{self.id}: {self.question_text[:50]}..."


class KeywordBlock(models.Model):
    """Model for keyword blocks in theory questions"""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='keyword_blocks')
    weight = models.FloatField(help_text="Weight percentage (0.0 to 1.0)")
    keywords = models.JSONField(default=list)  # List of keywords
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'keyword_blocks'
    
    def __str__(self):
        return f"Block {self.id} - Weight: {self.weight}"


class Response(models.Model):
    """Model to store student responses"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    confidence_level = models.IntegerField(null=True, blank=True)  # 1-5 scale
    time_taken = models.FloatField(help_text="Time taken in seconds")
    time_before_first_answer = models.FloatField(default=0.0)
    changed = models.BooleanField(default=False)
    revisited = models.BooleanField(default=False)
    mouse_clicks = models.IntegerField(default=0)
    focus_lost_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'responses'
        unique_together = ['user', 'test', 'question']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.id}"
