from django.urls import path
from . import views

urlpatterns = [
    # Analytics URLs will be added here
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    path('student/<int:user_id>/', views.student_analytics, name='student_analytics'),
    path('test/<int:test_id>/', views.test_analytics, name='test_analytics'),
    path('embed/<int:widget_id>/', views.embedded_widget, name='embedded_widget'),
]
