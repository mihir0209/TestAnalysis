from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentRegistrationForm, TeacherRegistrationForm, PreRegisterStudentForm, SubjectForm
from .models import PreRegisteredStudent, Subject
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    """Home page with role selection"""
    return render(request, 'accounts/home.html')


def student_login(request):
    """Student login page"""
    return render(request, 'accounts/student_login.html')


def teacher_login(request):
    """Teacher login page"""
    return render(request, 'accounts/teacher_login.html')


def student_register(request):
    """Student registration page"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('student_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/student_register.html', {'form': form})


def teacher_register(request):
    """Teacher registration page"""
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Teacher account created for {username}! You can now log in.')
            return redirect('teacher_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'accounts/teacher_register.html', {'form': form})


@login_required
def student_dashboard(request):
    """Student dashboard"""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Students only.')
        return redirect('home')
    
    # Import models here to avoid circular imports
    from rooms.models import Room, RoomParticipant
    from tests.models import Test, Response
    
    # Get student's rooms
    joined_rooms = Room.objects.filter(participants__student=request.user)
    
    # Get available tests (from joined rooms)
    available_tests = Test.objects.filter(room__in=joined_rooms).distinct()
    
    # Get taken tests
    taken_tests = Response.objects.filter(user=request.user).values_list('test_id', flat=True).distinct()
    
    # Calculate statistics
    total_rooms = joined_rooms.count()
    total_tests = available_tests.count()
    tests_taken = len(taken_tests)
    
    # Calculate average score
    responses = Response.objects.filter(user=request.user)
    if responses.exists():
        total_responses = responses.count()
        correct_responses = responses.filter(is_correct=True).count()
        average_score = (correct_responses / total_responses) * 100 if total_responses > 0 else 0
    else:
        average_score = 0
    
    # Get recent activity (placeholder)
    recent_activities = []
    
    context = {
        'user': request.user,
        'total_rooms': total_rooms,
        'total_tests': total_tests,
        'tests_taken': tests_taken,
        'average_score': average_score,
        'joined_rooms': joined_rooms[:5],  # Show only recent 5
        'available_tests': available_tests[:5],  # Show only recent 5
        'taken_test_ids': taken_tests,
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Teacher dashboard"""
    if not request.user.is_teacher():
        messages.error(request, 'Access denied. Teachers only.')
        return redirect('home')
    
    # Import models here to avoid circular imports
    from rooms.models import Room, RoomParticipant
    from tests.models import Test, Response
    
    # Get teacher's data
    subjects = Subject.objects.filter(teacher=request.user, is_active=True)
    registered_students = PreRegisteredStudent.objects.filter(registered_by=request.user)
    
    # Get rooms and tests data
    rooms = Room.objects.filter(teacher=request.user)
    tests = Test.objects.filter(created_by=request.user)
    
    # Get recent activity
    recent_rooms = rooms.order_by('-created_at')[:5]
    recent_tests = tests.order_by('-created_at')[:5]
    
    # Calculate statistics
    total_students_in_rooms = RoomParticipant.objects.filter(room__teacher=request.user).count()
    total_responses = Response.objects.filter(test__created_by=request.user).count()
    
    context = {
        'user': request.user,
        'subjects': subjects,
        'registered_students': registered_students,
        'total_subjects': subjects.count(),
        'total_students': registered_students.filter(is_used=True).count(),
        'pending_students': registered_students.filter(is_used=False).count(),
        'total_rooms': rooms.count(),
        'total_tests': tests.count(),
        'total_responses': total_responses,
        'recent_rooms': recent_rooms,
        'recent_tests': recent_tests,
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required
def pre_register_students(request):
    """Pre-register students view for teachers"""
    if not request.user.is_teacher():
        messages.error(request, 'Access denied. Teachers only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PreRegisterStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.registered_by = request.user
            student.save()
            messages.success(request, f'Student {student.student_id} pre-registered successfully!')
            return redirect('pre_register_students')
    else:
        form = PreRegisterStudentForm()
    
    students = PreRegisteredStudent.objects.filter(registered_by=request.user).order_by('-created_at')
    return render(request, 'accounts/pre_register_students.html', {
        'form': form,
        'students': students
    })


@login_required
def manage_subjects(request):
    """Manage subjects view for teachers"""
    if not request.user.is_teacher():
        messages.error(request, 'Access denied. Teachers only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            messages.success(request, f'Subject {subject.name} created successfully!')
            return redirect('manage_subjects')
    else:
        form = SubjectForm()
    
    subjects = Subject.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'accounts/manage_subjects.html', {
        'form': form,
        'subjects': subjects
    })


@csrf_exempt
def check_student_id(request):
    """AJAX endpoint to check if student ID is available"""
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        # Check if student ID exists in pre-registered list
        pre_registered = PreRegisteredStudent.objects.filter(student_id=student_id, is_used=False).exists()
        already_used = User.objects.filter(student_id=student_id).exists()
        
        return JsonResponse({
            'available': pre_registered and not already_used,
            'message': 'Available' if pre_registered and not already_used else 'Not available or already used'
        })
    
    return JsonResponse({'error': 'Invalid request'})
