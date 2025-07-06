from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Room, RoomParticipant
from accounts.models import User
import json


class RoomCreationForm(forms.ModelForm):
    """Form for creating new rooms"""
    
    class Meta:
        model = Room
        fields = ['name', 'description', 'entry_deadline', 'max_students', 'late_penalty', 'settings']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter room description (optional)'
            }),
            'entry_deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 500,
                'placeholder': 'Maximum number of students'
            }),
            'late_penalty': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.1,
                'min': 0,
                'placeholder': 'Penalty for late entry (0.0 to 1.0)'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional settings in JSON format (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields optional
        self.fields['description'].required = False
        self.fields['settings'].required = False
        
        # Set default values
        self.fields['max_students'].initial = 50
        self.fields['late_penalty'].initial = 0.1
    
    def clean_entry_deadline(self):
        """Validate entry deadline"""
        entry_deadline = self.cleaned_data.get('entry_deadline')
        if entry_deadline and entry_deadline <= timezone.now():
            raise ValidationError("Entry deadline must be in the future")
        return entry_deadline
    
    def clean_settings(self):
        """Validate settings JSON"""
        settings = self.cleaned_data.get('settings')
        if settings:
            try:
                json.loads(settings)
            except json.JSONDecodeError:
                raise ValidationError("Settings must be valid JSON format")
        return settings
    
    def clean_late_penalty(self):
        """Validate late penalty"""
        late_penalty = self.cleaned_data.get('late_penalty')
        if late_penalty and (late_penalty < 0 or late_penalty > 1):
            raise ValidationError("Late penalty must be between 0.0 and 1.0")
        return late_penalty


class JoinRoomForm(forms.Form):
    """Form for joining a room using invite code"""
    
    invite_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter room invite code',
            'style': 'text-transform: uppercase;'
        }),
        label="Invite Code"
    )
    
    def clean_invite_code(self):
        """Validate invite code"""
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code:
            invite_code = invite_code.upper()
            try:
                room = Room.objects.get(invite_code=invite_code)
                if not room.is_active:
                    raise ValidationError("This room is no longer active")
                return invite_code
            except Room.DoesNotExist:
                raise ValidationError("Invalid invite code")
        return invite_code


class RoomEditForm(forms.ModelForm):
    """Form for editing room details"""
    
    class Meta:
        model = Room
        fields = ['name', 'description', 'entry_deadline', 'max_students', 'late_penalty', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'entry_deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 500
            }),
            'late_penalty': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.1,
                'min': 0,
                'max': 1
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
    
    def clean_entry_deadline(self):
        """Validate entry deadline"""
        entry_deadline = self.cleaned_data.get('entry_deadline')
        if entry_deadline and entry_deadline <= timezone.now():
            raise ValidationError("Entry deadline must be in the future")
        return entry_deadline
    
    def clean_late_penalty(self):
        """Validate late penalty"""
        late_penalty = self.cleaned_data.get('late_penalty')
        if late_penalty and (late_penalty < 0 or late_penalty > 1):
            raise ValidationError("Late penalty must be between 0.0 and 1.0")
        return late_penalty


class RoomSettingsForm(forms.Form):
    """Form for advanced room settings"""
    
    auto_start_test = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Auto-start test when room is full"
    )
    
    require_approval = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Require teacher approval for students to join"
    )
    
    send_notifications = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Send email notifications to students"
    )
    
    allow_late_entry = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Allow students to join after deadline (with penalty)"
    )
    
    backup_room = forms.ModelChoiceField(
        queryset=Room.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Backup room (if this room fails)"
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['backup_room'].queryset = Room.objects.filter(
                teacher=user, is_active=True
            ).exclude(id=kwargs.get('instance', {}).get('id'))
