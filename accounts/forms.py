from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import PreRegisteredStudent, Subject

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    """Custom registration form for students"""
    
    student_id = forms.CharField(
        max_length=20,
        help_text="Enter your student ID (e.g., TY-4789)",
        widget=forms.TextInput(attrs={
            'placeholder': 'TY-4789',
            'pattern': '(FY|SY|TY|LY)-\\d{4}',
            'title': 'Format: YY-NNNN (e.g., TY-4789)'
        })
    )
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'student_id', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        
        # Check if student ID exists in pre-registered list
        if not PreRegisteredStudent.objects.filter(student_id=student_id, is_used=False).exists():
            raise forms.ValidationError(
                "This student ID is not registered or has already been used. "
                "Please contact your teacher for approval."
            )
        
        # Check if student ID is already used
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This student ID is already registered.")
        
        return student_id
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_approved = True  # Auto-approve if student ID is pre-registered
        
        if commit:
            user.save()
            # Mark the pre-registered student as used
            pre_reg = PreRegisteredStudent.objects.get(student_id=user.student_id)
            pre_reg.is_used = True
            pre_reg.used_by = user
            pre_reg.save()
            
            # Set year_of_study from pre-registered data
            user.year_of_study = pre_reg.year_of_study
            user.save()
        
        return user


class TeacherRegistrationForm(UserCreationForm):
    """Custom registration form for teachers"""
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_approved = True  # Auto-approve teachers
        
        if commit:
            user.save()
        
        return user


class PreRegisterStudentForm(forms.ModelForm):
    """Form for teachers to pre-register students"""
    
    class Meta:
        model = PreRegisteredStudent
        fields = ['student_id', 'full_name', 'year_of_study']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'placeholder': 'TY-4789',
                'pattern': '(FY|SY|TY|LY)-\\d{4}',
                'title': 'Format: YY-NNNN (e.g., TY-4789)'
            }),
            'full_name': forms.TextInput(attrs={'placeholder': 'Student Full Name'}),
        }
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        
        # Validate format
        import re
        if not re.match(r'^(FY|SY|TY|LY)-\d{4}$', student_id):
            raise forms.ValidationError("Invalid format. Use YY-NNNN (e.g., TY-4789)")
        
        # Check if already exists
        if PreRegisteredStudent.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This student ID is already registered.")
        
        return student_id


class SubjectForm(forms.ModelForm):
    """Form for creating/editing subjects"""
    
    class Meta:
        model = Subject
        fields = ['name', 'code', 'year_applicable']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Subject Name'}),
            'code': forms.TextInput(attrs={'placeholder': 'SUBJ101'}),
        }
