from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import models
from .models import Test, Question, Response, KeywordBlock
from .forms import TestCreationForm, QuestionForm, KeywordBlockForm, TestConfigurationForm
from rooms.models import Room
import json


@login_required
def test_list(request):
    """List all tests created by the current user"""
    if request.user.role != 'teacher':
        messages.error(request, "Access denied. Only teachers can view test lists.")
        return redirect('home')
    
    tests = Test.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tests': page_obj,
        'total_tests': tests.count(),
    }
    return render(request, 'tests/test_list.html', context)


@login_required
def create_test(request):
    """Create a new test"""
    if request.user.role != 'teacher':
        messages.error(request, "Access denied. Only teachers can create tests.")
        return redirect('home')
    
    if request.method == 'POST':
        form = TestCreationForm(request.POST, user=request.user)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            
            # Parse settings if provided
            settings = form.cleaned_data.get('settings')
            if settings:
                try:
                    test.settings = json.loads(settings)
                except json.JSONDecodeError:
                    test.settings = {}
            
            test.save()
            messages.success(request, f"Test '{test.title}' created successfully!")
            return redirect('test_detail', test_id=test.id)
    else:
        form = TestCreationForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Create New Test',
    }
    return render(request, 'tests/create_test.html', context)


@login_required
def test_detail(request, test_id):
    """View test details and manage questions"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permissions
    if request.user.role == 'teacher' and test.created_by != request.user:
        messages.error(request, "Access denied. You can only view your own tests.")
        return redirect('test_list')
    
    questions = test.questions.all().order_by('id')
    
    # Calculate test statistics
    total_questions = questions.count()
    total_marks = sum(q.marks for q in questions)
    avg_marks = total_marks / total_questions if total_questions > 0 else 0
    
    # Get response statistics (for teachers)
    response_stats = {}
    if request.user.role == 'teacher':
        responses = Response.objects.filter(test=test)
        response_stats = {
            'total_responses': responses.count(),
            'unique_students': responses.values('user').distinct().count(),
            'avg_score': responses.aggregate(avg=models.Avg('is_correct'))['avg'] or 0,
        }
    
    context = {
        'test': test,
        'questions': questions,
        'total_questions': total_questions,
        'total_marks': total_marks,
        'avg_marks': avg_marks,
        'response_stats': response_stats,
    }
    return render(request, 'tests/test_detail.html', context)


@login_required
def add_question(request, test_id):
    """Add a new question to a test"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permissions
    if request.user.role != 'teacher' or test.created_by != request.user:
        messages.error(request, "Access denied. You can only add questions to your own tests.")
        return redirect('test_detail', test_id=test_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            
            # Update test questions count
            test.questions_count = test.questions.count()
            test.save()
            
            messages.success(request, "Question added successfully!")
            return redirect('test_detail', test_id=test_id)
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'test': test,
        'title': f'Add Question to {test.title}',
    }
    return render(request, 'tests/add_question.html', context)


@login_required
def edit_question(request, test_id, question_id):
    """Edit an existing question"""
    test = get_object_or_404(Test, id=test_id)
    question = get_object_or_404(Question, id=question_id, test=test)
    
    # Check permissions
    if request.user.role != 'teacher' or test.created_by != request.user:
        messages.error(request, "Access denied. You can only edit questions in your own tests.")
        return redirect('test_detail', test_id=test_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('test_detail', test_id=test_id)
    else:
        form = QuestionForm(instance=question)
        
        # Convert options list back to text for editing
        if question.options:
            form.initial['options'] = '\n'.join(question.options)
        
        # Convert keywords dict back to JSON for editing
        if question.keywords:
            form.initial['keywords'] = json.dumps(question.keywords, indent=2)
    
    context = {
        'form': form,
        'test': test,
        'question': question,
        'title': f'Edit Question in {test.title}',
    }
    return render(request, 'tests/edit_question.html', context)


@login_required
def delete_question(request, test_id, question_id):
    """Delete a question"""
    test = get_object_or_404(Test, id=test_id)
    question = get_object_or_404(Question, id=question_id, test=test)
    
    # Check permissions
    if request.user.role != 'teacher' or test.created_by != request.user:
        messages.error(request, "Access denied. You can only delete questions from your own tests.")
        return redirect('test_detail', test_id=test_id)
    
    if request.method == 'POST':
        question.delete()
        
        # Update test questions count
        test.questions_count = test.questions.count()
        test.save()
        
        messages.success(request, "Question deleted successfully!")
        return redirect('test_detail', test_id=test_id)
    
    context = {
        'test': test,
        'question': question,
    }
    return render(request, 'tests/delete_question.html', context)


@login_required
def take_test(request, test_id):
    """Take a test (for students)"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check if user is a student
    if request.user.role != 'student':
        messages.error(request, "Access denied. Only students can take tests.")
        return redirect('home')
    
    # Check if student is in the test room
    if test.room and not test.room.participants.filter(student=request.user).exists():
        messages.error(request, "You must join the room first to take this test.")
        return redirect('room_detail', room_id=test.room.id)
    
    # Check if test has already been taken
    existing_responses = Response.objects.filter(user=request.user, test=test)
    if existing_responses.exists():
        messages.info(request, "You have already taken this test.")
        return redirect('test_results', test_id=test_id)
    
    questions = test.questions.all().order_by('id')
    
    if not questions.exists():
        messages.error(request, "This test has no questions yet.")
        return redirect('student_dashboard')
    
    context = {
        'test': test,
        'questions': questions,
        'total_questions': questions.count(),
    }
    return render(request, 'tests/take_test.html', context)


@login_required
def test_results(request, test_id):
    """View test results"""
    test = get_object_or_404(Test, id=test_id)
    
    if request.user.role == 'student':
        # Students can only see their own results
        responses = Response.objects.filter(user=request.user, test=test)
        if not responses.exists():
            messages.error(request, "You haven't taken this test yet.")
            return redirect('student_dashboard')
        
        # Calculate score
        total_questions = test.questions.count()
        correct_answers = responses.filter(is_correct=True).count()
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        context = {
            'test': test,
            'responses': responses,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score,
        }
        return render(request, 'tests/student_results.html', context)
    
    elif request.user.role == 'teacher' and test.created_by == request.user:
        # Teachers can see all results for their tests
        responses = Response.objects.filter(test=test).order_by('user__username', 'question__id')
        
        # Group responses by student
        student_results = {}
        for response in responses:
            if response.user.username not in student_results:
                student_results[response.user.username] = {
                    'user': response.user,
                    'responses': [],
                    'total_questions': 0,
                    'correct_answers': 0,
                    'score': 0,
                }
            student_results[response.user.username]['responses'].append(response)
            student_results[response.user.username]['total_questions'] += 1
            if response.is_correct:
                student_results[response.user.username]['correct_answers'] += 1
        
        # Calculate scores
        for username, data in student_results.items():
            if data['total_questions'] > 0:
                data['score'] = (data['correct_answers'] / data['total_questions']) * 100
        
        context = {
            'test': test,
            'student_results': student_results,
        }
        return render(request, 'tests/teacher_results.html', context)
    
    else:
        messages.error(request, "Access denied.")
        return redirect('home')
