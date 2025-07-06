from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('create/', views.create_room, name='create_room'),
    path('<int:room_id>/', views.room_detail, name='room_detail'),
    path('<int:room_id>/join/', views.join_room, name='join_room'),
    path('<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('<int:room_id>/leave/', views.leave_room, name='leave_room'),
    path('<int:room_id>/participants/<int:participant_id>/remove/', views.remove_participant, name='remove_participant'),
    path('join/', views.join_room_by_code, name='join_room_by_code'),
    path('join/<str:invite_code>/', views.join_room_by_code, name='join_room_by_code'),
]
