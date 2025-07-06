from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('create/', views.create_test, name='create_test'),
    path('<int:test_id>/', views.test_detail, name='test_detail'),
    path('<int:test_id>/take/', views.take_test, name='take_test'),
    path('<int:test_id>/results/', views.test_results, name='test_results'),
    path('<int:test_id>/add-question/', views.add_question, name='add_question'),
    path('<int:test_id>/questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('<int:test_id>/questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]
