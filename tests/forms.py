from django import forms
from django.core.exceptions import ValidationError
from .models import Test, Question, KeywordBlock
from rooms.models import Room
import json


class TestCreationForm(forms.ModelForm):
    """Form for creating new tests"""
    
    class Meta:
        model = Test
        fields = ['title', 'description', 'room', 'can_pause', 'analytics_mode', 'total_time', 'settings']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter test description (optional)'
            }),
            'room': forms.Select(attrs={
                'class': 'form-select'
            }),
            'can_pause': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'analytics_mode': forms.Select(attrs={
                'class': 'form-select'
            }),
            'total_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total time in minutes',
                'min': 1,
                'max': 300
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter additional settings in JSON format (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter rooms to only show those created by the current user
        if self.user:
            self.fields['room'].queryset = Room.objects.filter(teacher=self.user, is_active=True)
        
        # Make settings field optional
        self.fields['settings'].required = False
    
    def clean_settings(self):
        """Validate settings JSON"""
        settings = self.cleaned_data.get('settings')
        if settings:
            try:
                json.loads(settings)
            except json.JSONDecodeError:
                raise ValidationError("Settings must be valid JSON format")
        return settings
    
    def clean_total_time(self):
        """Validate total time"""
        total_time = self.cleaned_data.get('total_time')
        if total_time and total_time < 1:
            raise ValidationError("Total time must be at least 1 minute")
        return total_time


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""
    
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'options', 'correct_answer', 
                 'evaluation_type', 'keywords', 'keyword_threshold', 'difficulty_level', 'marks']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your question here'
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'options': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter options for MCQ (one per line)'
            }),
            'correct_answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter the correct answer'
            }),
            'evaluation_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter keywords for theory questions (JSON format)'
            }),
            'keyword_threshold': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.1,
                'min': 0,
                'max': 1
            }),
            'difficulty_level': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('easy', 'Easy'),
                ('medium', 'Medium'),
                ('hard', 'Hard')
            ]),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.5,
                'min': 0.5
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields optional based on question type
        self.fields['options'].required = False
        self.fields['keywords'].required = False
        self.fields['keyword_threshold'].required = False
    
    def clean_options(self):
        """Validate options for MCQ"""
        options = self.cleaned_data.get('options')
        question_type = self.cleaned_data.get('question_type')
        
        if question_type == 'mcq':
            if not options:
                raise ValidationError("Options are required for multiple choice questions")
            
            # Convert options to list format
            options_list = [opt.strip() for opt in options.split('\n') if opt.strip()]
            if len(options_list) < 2:
                raise ValidationError("At least 2 options are required for MCQ")
            
            return options_list
        
        return options if options else []
    
    def clean_keywords(self):
        """Validate keywords for theory questions"""
        keywords = self.cleaned_data.get('keywords')
        question_type = self.cleaned_data.get('question_type')
        evaluation_type = self.cleaned_data.get('evaluation_type')
        
        if question_type == 'theory' and evaluation_type == 'keyword':
            if not keywords:
                raise ValidationError("Keywords are required for keyword-based theory questions")
            
            try:
                keywords_dict = json.loads(keywords)
                if not isinstance(keywords_dict, dict):
                    raise ValidationError("Keywords must be a JSON object")
                return keywords_dict
            except json.JSONDecodeError:
                raise ValidationError("Keywords must be valid JSON format")
        
        return keywords if keywords else {}
    
    def clean(self):
        """Additional validation"""
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        evaluation_type = cleaned_data.get('evaluation_type')
        
        # Validate evaluation type based on question type
        if question_type == 'mcq' and evaluation_type != 'exact':
            raise ValidationError("MCQ questions must use exact match evaluation")
        
        return cleaned_data


class KeywordBlockForm(forms.ModelForm):
    """Form for creating keyword blocks"""
    
    class Meta:
        model = KeywordBlock
        fields = ['weight', 'keywords']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.1,
                'min': 0,
                'max': 1,
                'placeholder': 'Enter weight (0.0 to 1.0)'
            }),
            'keywords': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter keywords (one per line)'
            }),
        }
    
    def clean_keywords(self):
        """Convert keywords to list format"""
        keywords = self.cleaned_data.get('keywords')
        if keywords:
            keywords_list = [kw.strip() for kw in keywords.split('\n') if kw.strip()]
            if not keywords_list:
                raise ValidationError("At least one keyword is required")
            return keywords_list
        return []
    
    def clean_weight(self):
        """Validate weight"""
        weight = self.cleaned_data.get('weight')
        if weight and (weight < 0 or weight > 1):
            raise ValidationError("Weight must be between 0.0 and 1.0")
        return weight


class TestConfigurationForm(forms.Form):
    """Form for additional test configuration"""
    
    shuffle_questions = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Shuffle Questions"
    )
    
    shuffle_options = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Shuffle MCQ Options"
    )
    
    show_results_immediately = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Show Results Immediately After Test"
    )
    
    allow_review = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Allow Students to Review Answers"
    )
    
    max_attempts = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'placeholder': 'Maximum attempts (leave blank for unlimited)'
        }),
        label="Maximum Attempts"
    )
