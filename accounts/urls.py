from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and role selection
    path('', views.home, name='home'),
    
    # Student URLs
    path('student/login/', auth_views.LoginView.as_view(
        template_name='accounts/student_login.html',
        redirect_authenticated_user=True,
        extra_context={'user_type': 'student'}
    ), name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Teacher URLs
    path('teacher/login/', auth_views.LoginView.as_view(
        template_name='accounts/teacher_login.html',
        redirect_authenticated_user=True,
        extra_context={'user_type': 'teacher'}
    ), name='teacher_login'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/pre-register/', views.pre_register_students, name='pre_register_students'),
    path('teacher/subjects/', views.manage_subjects, name='manage_subjects'),
    
    # Common URLs
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # AJAX endpoints
    path('ajax/check-student-id/', views.check_student_id, name='check_student_id'),
]
